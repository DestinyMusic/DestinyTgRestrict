# ==============================================================================
# --- DATABASE ---
# ==============================================================================

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(
            uri,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            maxPoolSize=50
        )
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            session = None,
            api_id = None,
            api_hash = None,
        )

    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.update_one(
            {'id': int(id)},
            {'$setOnInsert': user},
            upsert=True
        )

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        cursor = self.col.find({})
        return cursor

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def set_session(self, id, session):
        await self.col.update_one({'id': int(id)}, {'$set': {'session': session}})

    async def get_session(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('session') if user else None

    async def set_api_id(self, id, api_id):
        await self.col.update_one({'id': int(id)}, {'$set': {'api_id': api_id}})

    async def get_api_id(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('api_id') if user else None

    async def set_api_hash(self, id, api_hash):
        await self.col.update_one({'id': int(id)}, {'$set': {'api_hash': api_hash}})

    async def get_api_hash(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('api_hash') if user else None

    async def total_session_users_count(self):
        count = await self.col.count_documents({"session": {"$ne": None}})
        return count

    async def get_monthly_bandwidth(self):
        """Tracks, persists, and auto-resets monthly bandwidth usage in MongoDB across server reboots."""
        current_month = datetime.datetime.now().strftime("%Y-%m")
        month_display = datetime.datetime.now().strftime("%B %Y")
        
        net = psutil.net_io_counters()
        cur_raw_rx = net.bytes_recv
        cur_raw_tx = net.bytes_sent
        
        doc = await self.db.config.find_one({"_id": "monthly_bandwidth"})
        
        if not doc or doc.get("month") != current_month:
            new_data = {
                "month": current_month,
                "rx_bytes": 0,
                "tx_bytes": 0,
                "last_raw_rx": cur_raw_rx,
                "last_raw_tx": cur_raw_tx
            }
            await self.db.config.update_one({"_id": "monthly_bandwidth"}, {"$set": new_data}, upsert=True)
            return 0, 0, 0, month_display
            
        last_raw_rx = doc.get("last_raw_rx", cur_raw_rx)
        last_raw_tx = doc.get("last_raw_tx", cur_raw_tx)
        
        delta_rx = cur_raw_rx if cur_raw_rx < last_raw_rx else (cur_raw_rx - last_raw_rx)
        delta_tx = cur_raw_tx if cur_raw_tx < last_raw_tx else (cur_raw_tx - last_raw_tx)
        
        rx_total = doc.get("rx_bytes", 0) + max(0, delta_rx)
        tx_total = doc.get("tx_bytes", 0) + max(0, delta_tx)
        
        await self.db.config.update_one(
            {"_id": "monthly_bandwidth"},
            {"$set": {
                "rx_bytes": rx_total,
                "tx_bytes": tx_total,
                "last_raw_rx": cur_raw_rx,
                "last_raw_tx": cur_raw_tx
            }}
        )
        return rx_total, tx_total, (rx_total + tx_total), month_display
        
    # --- WATCHER METHODS ---
    async def add_watcher(
        self,
        user_id,
        source_id,
        dest_id,
        source_thread=None,
        dest_thread=None,
        delay=3,
        is_restricted=False,
        source_title=None,
        dest_title=None,
        allowed_types=None,
        dashboard_chat=None,
        dashboard_msg=None,
        last_msg_id=0     # 🟢 ADD THIS PARAMETER
    ):
        if allowed_types is None:
            allowed_types = ["Video", "Document"]

        query = {
            "user_id": int(user_id),
            "source_id": int(source_id),
            "source_thread": int(source_thread) if source_thread is not None else None,
            "dest_id": int(dest_id),                                             # <-- ADDED
            "dest_thread": int(dest_thread) if dest_thread is not None else None # <-- ADDED
        }
        
        update_data = {
            "user_id": int(user_id),
            "source_id": int(source_id),
            "dest_id": int(dest_id),
            "source_thread": int(source_thread) if source_thread is not None else None,
            "dest_thread": int(dest_thread) if dest_thread is not None else None,
            "delay": int(delay),
            "is_restricted": bool(is_restricted),
            "source_title": source_title,
            "dest_title": dest_title,
            "allowed_types": allowed_types,
            "dashboard_chat": dashboard_chat,
            "dashboard_msg": dashboard_msg,
            "created_at": datetime.datetime.now()
        }

        # $setOnInsert ensures stats are created only on the first run and not reset on updates
        await self.db.watchers.update_one(
            query, 
            {
                "$set": update_data,
                "$setOnInsert": {
                    "stats": {"detected": 0, "success": 0, "skipped": 0, "failed": 0},
                    "last_msg_id": last_msg_id   # 🟢 SAVE THE STARTING ID
                }
            }, 
            upsert=True
        )

    async def get_user_watchers(self, user_id):
        return self.db.watchers.find({"user_id": int(user_id)})

    async def get_watchers_for_source(self, source_id, source_thread=None):
        query = {"source_id": int(source_id)}
        if source_thread is None:
            query["source_thread"] = None
        else:
            query["source_thread"] = int(source_thread)
        return self.db.watchers.find(query)

    async def get_all_watchers(self):
        return self.db.watchers.find({})

    async def remove_watcher(self, user_id, source_id, source_thread=None):
        query = {
            "user_id": int(user_id),
            "source_id": int(source_id)
        }

        if source_thread is None:
            result = await self.db.watchers.delete_many({
                "$or": [
                    {**query, "source_thread": None},
                    {**query, "source_thread": {"$exists": False}}
                ]
            })
        else:
            query["source_thread"] = int(source_thread)
            result = await self.db.watchers.delete_many(query)

        return result.deleted_count > 0

    # ==========================================
    # --- BATCH TASKS (AUTO-RESUME) METHODS ---
    # ==========================================
    async def add_active_task(self, task_uuid, user_id, link, dest_chat_id, dest_thread_id, dest_title, delay, is_restricted, allowed_types, source_title, current_msg_id, to_id):
        task_data = {
            "task_uuid": task_uuid, "user_id": user_id, "link": link,
            "dest_chat_id": dest_chat_id, "dest_thread_id": dest_thread_id,
            "dest_title": dest_title, "delay": delay, "is_restricted": is_restricted,
            "allowed_types": allowed_types, "source_title": source_title,
            "current_msg_id": current_msg_id, "to_id": to_id
        }
        await self.db.active_tasks.update_one({"task_uuid": task_uuid}, {"$set": task_data}, upsert=True)

    async def update_task_progress(self, task_uuid, current_msg_id):
        await self.db.active_tasks.update_one({"task_uuid": task_uuid}, {"$set": {"current_msg_id": current_msg_id}})

    async def remove_active_task(self, task_uuid):
        await self.db.active_tasks.delete_one({"task_uuid": task_uuid})

    async def get_all_active_tasks(self):
        return self.db.active_tasks.find({})

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(
            uri,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            maxPoolSize=50
        )
        self.db = self._client[database_name]
        self.col = self.db.users
        
        # 🟢 Added Memory Cache Variables
        self._access_cache = None
        self._access_cache_time = 0

    async def get_access_control(self):
        now = time.time()
        # 🟢 Return memory cache if less than 60 seconds old
        if self._access_cache and (now - self._access_cache_time) < 60:
            return self._access_cache
            
        doc = await self.db.config.find_one({"_id": "access_control"}) or {}
        revoked = doc.get("revoked_users", [])
        approved = doc.get("approved_users", [])
        dyn_admins = doc.get("dynamic_admins", [])
        dyn_sudos = doc.get("dynamic_sudos", [])
        
        # Calculate effective roles (combining .env hardcoded + MongoDB dynamic, filtering revoked)
        effective_admins = list(set([x for x in ADMINS if x not in revoked] + [x for x in dyn_admins if x not in revoked]))
        effective_sudos = list(set([x for x in SUDOS if x not in revoked] + [x for x in dyn_sudos if x not in revoked]))
        
        # 🟢 Save to Cache before returning
        self._access_cache = (effective_admins, effective_sudos, approved, revoked)
        self._access_cache_time = now
        
        return self._access_cache

    async def is_user_approved(self, user_id):
        user_id = int(user_id)
        effective_admins, effective_sudos, approved, _ = await self.get_access_control()
        if user_id in effective_admins or user_id in effective_sudos:
            return True
        return user_id in approved

    async def is_user_admin(self, user_id):
        user_id = int(user_id)
        effective_admins, effective_sudos, _, _ = await self.get_access_control()
        return user_id in effective_admins or user_id in effective_sudos

    async def add_approved_user(self, user_id, role="User"):
        user_id = int(user_id)
        # 1. Safely remove user from ALL groups to prevent overlapping roles
        await self.db.config.update_one(
            {"_id": "access_control"},
            {"$pull": {
                "revoked_users": user_id,
                "approved_users": user_id,
                "dynamic_admins": user_id,
                "dynamic_sudos": user_id
            }},
            upsert=True
        )
        
        # 2. Add them to the specifically requested role array
        target_array = "approved_users"
        if role == "Admin": target_array = "dynamic_admins"
        elif role == "Sudo": target_array = "dynamic_sudos"
        
        await self.db.config.update_one(
            {"_id": "access_control"},
            {"$addToSet": {target_array: user_id}},
            upsert=True
        )

    async def remove_user_access(self, user_id):
        user_id = int(user_id)
        await self.db.config.update_one(
            {"_id": "access_control"},
            {
                "$addToSet": {"revoked_users": user_id},
                "$pull": {
                    "approved_users": user_id,
                    "dynamic_admins": user_id,
                    "dynamic_sudos": user_id
                }
            },
            upsert=True
        )

db = Database(DB_URI, DB_NAME)
