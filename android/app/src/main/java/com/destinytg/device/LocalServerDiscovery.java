package com.destinytg.device;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public final class LocalServerDiscovery {
    private LocalServerDiscovery() {
    }

    public static List<String> buildCandidateAddresses(String preferred) {
        Set<String> candidates = new LinkedHashSet<>();

        if (preferred != null && !preferred.trim().isEmpty()) {
            String normalized = normalize(preferred);
            if (normalized != null) {
                candidates.add(normalized);
            }
        }

        addCandidates(candidates, "http://localhost:8080");
        addCandidates(candidates, "http://127.0.0.1:8080");
        addCandidates(candidates, "http://127.0.0.1:8000");

        List<String> commonLanBases = Arrays.asList(
                "192.168.1.1",
                "192.168.0.1",
                "10.0.0.1",
                "10.0.2.1",
                "172.16.0.1",
                "172.31.0.1",
                "192.168.50.1",
                "192.168.10.1",
                "192.168.2.1"
        );

        for (String base : commonLanBases) {
            addLanRange(candidates, base, 1, 32);
        }

        return new ArrayList<>(candidates);
    }

    private static void addCandidates(Set<String> candidates, String url) {
        String normalized = normalize(url);
        if (normalized != null) {
            candidates.add(normalized);
        }
    }

    private static void addLanRange(Set<String> candidates, String baseAddress, int start, int end) {
        String[] octets = baseAddress.split("\\.");
        if (octets.length != 4) {
            return;
        }

        int prefix = parseIntOrDefault(octets[0], 192);
        int second = parseIntOrDefault(octets[1], 168);
        int third = parseIntOrDefault(octets[2], 1);

        for (int host = start; host <= end; host++) {
            for (String scheme : Arrays.asList("http", "https")) {
                candidates.add(scheme + "://" + prefix + "." + second + "." + third + "." + host + ":8080");
            }
        }
    }

    private static int parseIntOrDefault(String value, int fallback) {
        try {
            return Integer.parseInt(value);
        } catch (NumberFormatException e) {
            return fallback;
        }
    }

    private static String normalize(String raw) {
        String value = raw == null ? "" : raw.trim();
        if (value.isEmpty()) {
            return null;
        }

        if (!value.contains("://")) {
            value = "http://" + value;
        }

        try {
            java.net.URI uri = new java.net.URI(value);
            String scheme = uri.getScheme();
            if (uri.getHost() == null || !("http".equalsIgnoreCase(scheme) || "https".equalsIgnoreCase(scheme))) {
                return null;
            }
            String path = uri.getRawPath();
            while (path != null && path.endsWith("/") && !path.isEmpty()) {
                path = path.substring(0, path.length() - 1);
            }
            return uri.getScheme() + "://" + uri.getRawAuthority() + (path == null ? "" : path);
        } catch (Exception ignored) {
            return null;
        }
    }
}
