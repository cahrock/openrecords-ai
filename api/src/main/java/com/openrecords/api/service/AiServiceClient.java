package com.openrecords.api.service;

import com.openrecords.api.config.AiServiceProperties;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;
import java.util.Optional;

@Component
public class AiServiceClient {

    private static final Logger log = LoggerFactory.getLogger(AiServiceClient.class);

    private final RestTemplate restTemplate;
    private final AiServiceProperties props;

    public AiServiceClient(AiServiceProperties props, RestTemplateBuilder builder) {
        this.props = props;
        this.restTemplate = builder
                .rootUri(props.baseUrl())
                .connectTimeout(Duration.ofSeconds(props.timeoutSeconds()))
                .readTimeout(Duration.ofSeconds(props.timeoutSeconds()))
                .build();
    }

    public boolean isHealthy() {
        try {
            var response = restTemplate.getForObject("/api/v1/health", HealthResponse.class);
            return response != null && "ok".equals(response.status());
        } catch (RestClientException e) {
            log.warn("AI service health check failed: {}", e.getMessage());
            return false;
        }
    }

    public record HealthResponse(String status, String service) {}
}