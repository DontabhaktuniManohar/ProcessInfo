package ReqRes;

import io.prometheus.client.CollectorRegistry;
import io.prometheus.client.Gauge;
import io.prometheus.client.exporter.PushGateway;

import java.io.IOException;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

public class KarateMetricsPusher {

    private static final String PUSHGATEWAY_URL = "http://localhost:9091"; // Must be passed as URL, not String to PushGateway

    private static final String JOB_NAME = "karate_test_suite";

    public static void pushFeatureMetrics(String featureName, int total, int passed, int failed) {
        CollectorRegistry registry = new CollectorRegistry();

        // Total scenarios
        Gauge totalGauge = Gauge.build()
                .name("karate_scenarios_total")
                .help("Total scenarios in the feature")
                .labelNames("feature")
                .register(registry);
        totalGauge.labels(featureName).set(total);

        // Passed scenarios
        Gauge passedGauge = Gauge.build()
                .name("karate_scenarios_passed")
                .help("Passed scenarios in the feature")
                .labelNames("feature")
                .register(registry);
        passedGauge.labels(featureName).set(passed);

        // Failed scenarios
        Gauge failedGauge = Gauge.build()
                .name("karate_scenarios_failed")
                .help("Failed scenarios in the feature")
                .labelNames("feature")
                .register(registry);
        failedGauge.labels(featureName).set(failed);

        try {
            PushGateway pushGateway = new PushGateway(new URL(PUSHGATEWAY_URL));

            // Use grouping key to differentiate metrics (but not duplicate them)
            Map<String, String> groupingKey = new HashMap<>();
            groupingKey.put("feature", featureName);

            // Use pushAdd to append (instead of overwriting)
            pushGateway.pushAdd(registry, JOB_NAME, groupingKey);

            System.out.println("✅ Metrics pushed for: " + featureName);
        } catch (IOException e) {
            System.err.println("❌ Failed to push metrics for " + featureName + ": " + e.getMessage());
            e.printStackTrace();
        }
    }
}
