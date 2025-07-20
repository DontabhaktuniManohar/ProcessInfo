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




package your.package.name;

import com.intuit.karate.Results;
import com.intuit.karate.Runner;
import com.intuit.karate.core.FeatureResult;
import com.intuit.karate.core.ScenarioResult;
import io.prometheus.client.Counter;
import io.prometheus.client.Gauge;
import io.prometheus.client.exporter.HTTPServer;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.util.List;
import java.util.stream.Collectors;

public class TestRunner {

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
        System.out.println("✅ Prometheus metrics server started on port: " + PROMETHEUS_PORT);
    }

    @AfterAll
    static void stopPrometheus() {
        if (prometheusServer != null) {
            prometheusServer.stop();
            System.out.println("🛑 Prometheus metrics server stopped.");
        }
    }

    @Test
    void runKarateTests() {
        testExecutionStatus.set(1);

        Results results = Runner.path("classpath:features")  // ✅ Adjust path to your feature directory
                .parallel(Runtime.getRuntime().availableProcessors());

        List<FeatureResult> featureResults = results.getFeatureResults()
                .collect(Collectors.toList()); // 🔄 Convert stream to list

        for (FeatureResult feature : featureResults) {
            String featureName = feature.getDisplayName();

            for (ScenarioResult scenario : feature.getScenarioResults()) {
                String scenarioName = scenario.getScenario().getName(); // ✅ Safe method

                if (scenario.isFailed()) {
                    testFailure.labels(featureName, scenarioName).inc();
                } else {
                    testPass.labels(featureName, scenarioName).inc();
                }
            }
        }

        testExecutionStatus.set(0);

        System.out.printf("✅ Karate Test Summary: Passed = %d, Failed = %d, Total = %d%n",
                results.getScenariosPassed(),
                results.getScenariosFailed(),
                results.getScenariosTotal());
    }
}

writePrometheusMetricsToFile(); // 👈 Add this
testExecutionStatus.set(0);


import io.prometheus.client.Collector;
import io.prometheus.client.CollectorRegistry;
import java.io.FileWriter;
import java.io.IOException;

private void writePrometheusMetricsToFile() {
    String fileName = "karate-prometheus-metrics.txt";
    try (FileWriter writer = new FileWriter(fileName)) {
        StringBuilder builder = new StringBuilder();
        for (Collector.MetricFamilySamples samples : CollectorRegistry.defaultRegistry.metricFamilySamples()) {
            builder.append("# HELP ").append(samples.name).append(" ").append(samples.help).append("\n");
            builder.append("# TYPE ").append(samples.name).append(" ").append(samples.type.name().toLowerCase()).append("\n");
            for (Collector.MetricFamilySamples.Sample sample : samples.samples) {
                builder.append(sample.name);
                if (!sample.labelNames.isEmpty()) {
                    builder.append("{");
                    for (int i = 0; i < sample.labelNames.size(); i++) {
                        builder.append(sample.labelNames.get(i)).append("=\"").append(sample.labelValues.get(i)).append("\"");
                        if (i < sample.labelNames.size() - 1) {
                            builder.append(",");
                        }
                    }
                    builder.append("}");
                }
                builder.append(" ").append(sample.value).append("\n");
            }
        }
        writer.write(builder.toString());
        System.out.println("📝 Prometheus metrics written to: " + fileName);
    } catch (IOException e) {
        e.printStackTrace();
    }
}