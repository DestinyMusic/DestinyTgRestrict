package com.destinytg.device;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

import java.util.List;

public class LocalServerDiscoveryTest {
    @Test
    public void buildCandidateAddressesIncludesLocalFallbacks() {
        List<String> candidates = LocalServerDiscovery.buildCandidateAddresses("http://192.168.1.20:8080");

        assertTrue(candidates.contains("http://192.168.1.20:8080"));
        assertTrue(candidates.contains("http://localhost:8080"));
        assertTrue(candidates.contains("http://192.168.1.1:8080"));
        assertFalse(candidates.isEmpty());
    }

    @Test
    public void buildCandidateAddressesAcceptsPlainHostValue() {
        List<String> candidates = LocalServerDiscovery.buildCandidateAddresses("192.168.1.50");
        assertTrue(candidates.contains("http://192.168.1.50"));
    }
}
