# ==============================================================================
# --- THE ULTIMATE FORENSIC & MASTERING AUDIO ANALYZER ---
# ==============================================================================

def get_channel_info_dsp(file_path):
    try:
        cmd = ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=channels,channel_layout,codec_name", "-of", "json", str(file_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        info = json.loads(result.stdout)['streams'][0]
        
        channels = info.get('channels', 2)
        layout = info.get('channel_layout', 'unknown').lower()
        codec = info.get('codec_name', '').lower()

        codec_map = {'alac': 'ALAC', 'aac': 'AAC', 'flac': 'FLAC', 'mp3': 'MP3', 'eac3': 'E-AC-3', 'ac4': 'AC-4', 'truehd': 'TrueHD', 'opus': 'OPUS', 'vorbis': 'OGG', 'pcm_s16le': 'WAV'}
        detected_format = codec_map.get(codec, codec.upper() if codec else "AUDIO")

        is_spatial = False
        if codec in ['eac3', 'ac4', 'truehd']:
            is_spatial = True
            channel_str = f"{channels} Ch (Binaural Downmix)" if 'binaural' in layout else f"{channels} Ch (Spatial / Atmos)"
        elif layout != 'unknown':
            channel_str = f"{channels} Ch ({layout.title()})"
        else:
            channel_str = f"{channels} Ch"

        return detected_format, channel_str, is_spatial
    except Exception: return "AUDIO", "2.0 Ch (Stereo)", False

def analyze_mastering(data, sr):
    try:
        if data.ndim == 1: data = np.expand_dims(data, axis=1)
        samples, channels = data.shape

        dc_offset_db = 20 * np.log10(np.abs(np.mean(data, axis=0)) + 1e-12)
        worst_dc = np.max(dc_offset_db)

        peak_db = 20 * np.log10(np.max(np.abs(data), axis=0) + 1e-12)
        max_peak = np.max(peak_db)
        rms_db = 20 * np.log10(np.sqrt(np.mean(data**2, axis=0)) + 1e-12)
        avg_rms = np.mean(rms_db)

        clip_events = 0
        for ch in range(channels):
            is_clip = (np.abs(data[:, ch]) >= 0.997).astype(int)
            if len(is_clip) >= 3:
                seq = np.convolve(is_clip, np.ones(3), mode='valid')
                clip_events += np.sum(seq == 3)

        correlation = 1.0
        if channels >= 2:
            c1, c2 = data[:, 0] - np.mean(data[:, 0]), data[:, 1] - np.mean(data[:, 1])
            den = np.sqrt(np.sum(c1**2) * np.sum(c2**2))
            if den > 0: correlation = np.sum(c1 * c2) / den

        lufs = -70.0
        if HAS_PYLN:
            meter = pyln.Meter(sr)
            lufs = meter.integrated_loudness(data)

        dr_channels = []
        for ch in range(channels):
            ch_data = data[:, ch]
            block_samples = 3 * sr
            num_blocks = len(ch_data) // block_samples
            if num_blocks > 1:
                rms_blocks = [np.sqrt(2 * np.mean(ch_data[i*block_samples:(i+1)*block_samples]**2) + 1e-12) for i in range(num_blocks)]
                peak_blocks = [np.max(np.abs(ch_data[i*block_samples:(i+1)*block_samples])) for i in range(num_blocks)]
                top_indices = np.argsort(rms_blocks)[::-1][:max(1, int(num_blocks * 0.2))]
                avg_top_rms = np.mean([rms_blocks[i] for i in top_indices])
                top_peaks = sorted([peak_blocks[i] for i in top_indices], reverse=True)
                if avg_top_rms > 0:
                    dr_channels.append(20 * np.log10((top_peaks[1] if len(top_peaks) > 1 else top_peaks[0]) / avg_top_rms))
        dr_val = max(1, int(round(np.mean(dr_channels)))) if dr_channels else 0

        grade = "🟢 Excellent" if (dr_val >= 11 and clip_events == 0) else ("🟡 Good / Moderate" if dr_val >= 8 and clip_events <= 50 else "🔴 Poor (Hot Master / Clipped)")
        return {"dc_offset": round(worst_dc, 1), "peak": round(max_peak, 2), "rms": round(avg_rms, 2), "clipping": clip_events, "correlation": round(correlation, 2), "lufs": round(lufs, 1), "dr": dr_val, "grade": grade}
    except Exception: return None

def detect_fake_24bit(data_raw, sr):
    try:
        mono = data_raw.mean(axis=1) if data_raw.ndim > 1 else data_raw
        frame_len = sr
        n_frames = len(mono) // frame_len
        if n_frames < 3: return "n/a", 0.0, "Track too short."
        frame_rms = np.array([np.sqrt(np.mean(mono[i*frame_len:(i+1)*frame_len] ** 2) + 1e-18) for i in range(n_frames)])
        loud_sample = np.concatenate([mono[i*frame_len:(i+1)*frame_len] for i in np.argsort(frame_rms)[::-1][:max(1, n_frames // 4)]])
        scaled = loud_sample * 32768.0
        on_grid_ratio = float(np.mean(np.abs(scaled - np.round(scaled)) < 1e-3))
        noise_floor_db = 20 * np.log10(np.std(np.concatenate([mono[i*frame_len:(i+1)*frame_len] for i in np.argsort(frame_rms)[:max(1, n_frames // 10)]])) + 1e-12)

        if on_grid_ratio > 0.98: return "padded", 0.95, f"{on_grid_ratio*100:.1f}% samples on 16-bit grid (Padded upscale)."
        if noise_floor_db >= -60.0: return "genuine", 0.50, f"No silent sections found (quietest is {noise_floor_db:.1f} dB). Assumed genuine."
        if noise_floor_db > -98.0: return "dithered_upscale", round(min(0.9, max(0.5, (noise_floor_db + 110) / 20)), 2), f"Noise floor {noise_floor_db:.1f} dB matches 16-bit dither."
        return "genuine", 0.85, f"Noise floor {noise_floor_db:.1f} dB matches 24-bit."
    except Exception: return "n/a", 0.0, "Analysis failed."

def generate_audio_stats_dsp(wav_path, original_file_path, original_name):
    try:
        audio = MutagenFile(original_file_path, easy=True)
        full = MutagenFile(original_file_path)
        title = audio.get('title', [original_name])[0] if audio else original_name
        artist = audio.get('artist', ['Unknown Artist'])[0] if audio else "Unknown Artist"
        bit_depth = getattr(full.info, "bits_per_sample", 16) if hasattr(full, 'info') else 16
        sample_rate_meta = getattr(full.info, "sample_rate", 44100) if hasattr(full, 'info') else 44100
    except Exception: title, artist, bit_depth, sample_rate_meta = original_name, "Unknown Artist", 16, 44100

    format_name, channel_str, is_spatial = get_channel_info_dsp(original_file_path)

    try:
        sr, data_raw = wavfile.read(wav_path)
        bit_verdict, bit_confidence, bit_detail = ("n/a", 0.0, "") if bit_depth != 24 else detect_fake_24bit(data_raw, sr)
        mastering = analyze_mastering(data_raw, sr)

        if data_raw.ndim > 1:
            f, t, Zxx_L = stft(data_raw[:, 0], fs=sr, nperseg=8192)
            f, t, Zxx_R = stft(data_raw[:, 1], fs=sr, nperseg=8192)
            max_mag = np.maximum(np.max(np.abs(Zxx_L), axis=1), np.max(np.abs(Zxx_R), axis=1))
            stft_2d = np.maximum(np.abs(Zxx_L), np.abs(Zxx_R))
        else:
            f, t, Zxx = stft(data_raw, fs=sr, nperseg=8192)
            max_mag, stft_2d = np.max(np.abs(Zxx), axis=1), np.abs(Zxx)

        psd_db = 20 * np.log10(max_mag + 1e-12)
        nyquist_hz = sr / 2.0
        passband_mask = (f >= 1000) & (f <= 8000)
        rel_psd_db = psd_db - (np.mean(psd_db[passband_mask]) if np.any(passband_mask) else np.max(psd_db))

        search_mask = f >= 10000
        search_freqs, search_db = f[search_mask], rel_psd_db[search_mask]
        noise_eval_mask = search_freqs >= (nyquist_hz * 0.85)
        dynamic_threshold = max(-60.0, min(-35.0, (np.median(search_db[noise_eval_mask]) if np.any(noise_eval_mask) else -55.0) + 12.0))

        cutoff_hz, consecutive_bins, required_bins = nyquist_hz, 0, max(1, int(150 / (sr / 8192)))
        for i in range(len(search_db) - 1, -1, -1):
            if search_db[i] > dynamic_threshold:
                consecutive_bins += 1
                if consecutive_bins >= required_bins: cutoff_hz = search_freqs[i + consecutive_bins - 1]; break
            else: consecutive_bins = 0

        pre_mask = (f >= max(0, cutoff_hz - 1500)) & (f <= cutoff_hz)
        post_mask = (f > cutoff_hz) & (f <= min(nyquist_hz, cutoff_hz + 1500))
        cliff_drop = float(np.median(rel_psd_db[pre_mask]) - np.median(rel_psd_db[post_mask])) if np.any(pre_mask) and np.any(post_mask) else 0.0

        hole_ratio = 0.0
        high_band_mask = (f >= 12000) & (f <= min(20000, nyquist_hz - 500))
        if np.any(high_band_mask):
            peak_val = np.max(stft_2d[high_band_mask, :])
            if peak_val > 0: hole_ratio = float(np.mean(stft_2d[high_band_mask, :] < (peak_val * 1e-4)))

        lossless_formats = ['FLAC', 'ALAC', 'WAV', 'PCM', 'DSF', 'DSD', 'AIFF']
        if is_spatial or format_name in ['E-AC-3', 'AC-4', 'TRUEHD']: auth_badge, auth_desc = "🟢 Dolby Atmos / Spatial", "Genuine spatial audio stream."
        elif format_name in lossless_formats:
            if bit_verdict == "padded": auth_badge, auth_desc = f"🔴 Fake 24-Bit / Padded ({bit_confidence*100:.0f}%)", bit_detail
            elif bit_verdict == "dithered_upscale": auth_badge, auth_desc = f"🟡 Possible Dithered Upscale ({bit_confidence*100:.0f}%)", bit_detail
            elif sample_rate_meta >= 88200 and (cutoff_hz/1000.0) >= 24.0: auth_badge, auth_desc = "🟢 Hi-Res Lossless", f"Genuine extension to {cutoff_hz/1000.0} kHz."
            elif hole_ratio > 0.15 and cliff_drop < 15.0 and (cutoff_hz/1000.0) >= 19.0: auth_badge, auth_desc = "🔴 Fake Lossless (Lossy)", f"Spectral hole {hole_ratio*100:.1f}%. Typical AAC/Opus transcode."
            elif cliff_drop >= 18.0 and (cutoff_hz/1000.0) <= 20.5 and mastering and mastering['clipping'] > 50: auth_badge, auth_desc = "🟢 Lossless · CD Quality (Hot Master)", "Clipping generated harmonics."
            elif cliff_drop >= 18.0 and (cutoff_hz/1000.0) <= 20.5: auth_badge, auth_desc = "🔴 Fake Lossless / Upscale", "Hard brick-wall cliff detected."
            elif (cutoff_hz/1000.0) > 20.0 or cliff_drop < 16.0: auth_badge, auth_desc = f"🟢 Lossless · {'Studio Master (24-bit)' if bit_depth == 24 else 'CD Quality'}", "Clean high-frequency response."
            else: auth_badge, auth_desc = "🟡 Inconclusive / Filtered", "Unusual slope detected."
        else:
            auth_badge, auth_desc = ("🟢 Standard Lossy", "Normal brick-wall detected.") if cliff_drop >= 18.0 else ("🟢 High-Bitrate Lossy", "Gradual roll-off. Excellent quality.")

        return {"title": title, "artist": artist, "format": format_name, "bit_depth": bit_depth, "sample_rate": sample_rate_meta, "channel_str": channel_str, "cutoff": round(cutoff_hz/1000.0, 1), "cliff_drop": round(cliff_drop, 1), "auth_badge": auth_badge, "auth_desc": auth_desc, "mastering": mastering}
    except Exception as e: return None

