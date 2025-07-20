import com.intuit.karate.Results;
import com.intuit.karate.Runner;
import com.intuit.karate.core.FeatureResult;
import com.intuit.karate.core.ScenarioResult;
import io.prometheus.client.Counter;
import io.prometheus.client.Gauge;
import io.prometheus.client.exporter.HTTPServer;
import io.prometheus.client.CollectorRegistry;

import org.junit.jupiter.api.*;

import java.io.IOException;

public class KarateMetricsRunner {

    private static HTTPServer prometheusServer;
    private static final int PROMETHEUS_PORT = 8081;

    private static final Counter testPass = Counter.build()
            .name("karate_test_pass_total")
            .help("Total passed Karate test scenarios")
            .labelNames("feature", "scenario")
            .register();

    private static final Counter testFailure = Counter.build()
            .name("karate_test_failure_total")
            .help("Total failed Karate test scenarios")
            .labelNames("feature", "scenario")
            .register();

    private static final Gauge testExecutionStatus = Gauge.build()
            .name("karate_test_execution_status")
            .help("Karate test execution status (1=running, 0=done)")
            .register();

    @BeforeAll
    static void startPrometheus() throws IOException {
        prometheusServer = new HTTPServer(PROMETHEUS_PORT);
        System.out.println("Prometheus metrics server started on port: " + PROMETHEUS_PORT);
    }

    @AfterAll
    static void stopPrometheus() {
        if (prometheusServer != null) {
            prometheusServer.stop();
            System.out.println("Prometheus metrics server stopped");
        }
    }

    @Test
    void runKarateTests() {
        testExecutionStatus.set(1);

        Results results = Runner.path("classpath:features")
                .parallel(Runtime.getRuntime().availableProcessors());

        for (FeatureResult feature : results.getFeatureResults()) {
            String featureName = feature.getDisplayName();

            for (ScenarioResult scenario : feature.getScenarioResults()) {
                String scenarioName = scenario.getDisplayMeta();

                if (scenario.isFailed()) {
                    testFailure.labels(featureName, scenarioName).inc();
                } else {
                    testPass.labels(featureName, scenarioName).inc();
                }
            }
        }

        testExecutionStatus.set(0);
        System.out.println("Total: " + results.getScenariosTotal()
                + ", Passed: " + results.getScenariosPassed()
                + ", Failed: " + results.getScenariosFailed());
    }
}