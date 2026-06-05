package com.openrecords.api.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "openrecords.ai-service")
public record AiServiceProperties(
        String baseUrl,
        int timeoutSeconds
) {}