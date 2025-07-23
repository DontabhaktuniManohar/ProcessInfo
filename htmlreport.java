package ReqRes;

import com.intuit.karate.core.FeatureResult;
import com.intuit.karate.core.ScenarioResult;

import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

public class FailedScenarioReporter {

    public static int generate(List<FeatureResult> featureResults) {
        StringBuilder html = new StringBuilder();
        html.append("<html><head><title>Failed Scenarios</title>")
            .append("<style>body{font-family:sans-serif;}table{border-collapse:collapse;width:100%;}th,td{border:1px solid #ccc;padding:8px;}th{background:#eee;}</style>")
            .append("</head><body><h2>❌ Failed Scenarios Report</h2>")
            .append("<table><tr><th>Feature File</th><th>Scenario Name</th><th>Line Number</th></tr>");

        int totalFailures = 0;

        for (FeatureResult feature : featureResults) {
            String featurePath = feature.getFeature().getResource().getPath();

            for (ScenarioResult scenario : feature.getScenarioResults()) {
                if (scenario.isFailed()) {
                    totalFailures++;
                    String name = scenario.getScenario().getName();
                    int line = scenario.getScenario().getLine();

                    html.append("<tr>")
                        .append("<td>").append(featurePath).append("</td>")
                        .append("<td>").append(name).append("</td>")
                        .append("<td>").append(line).append("</td>")
                        .append("</tr>");
                }
            }
        }

        html.append("</table>");

        if (totalFailures == 0) {
            html.append("<p style='color:green;'>🎉 All scenarios passed!</p>");
        } else {
            html.append("<p style='color:red;'>Total Failed Scenarios: ").append(totalFailures).append("</p>");
        }

        html.append("</body></html>");

        try (FileWriter writer = new FileWriter("target/failed-scenarios.html")) {
            writer.write(html.toString());
            System.out.println("✅ HTML failed scenario report created: target/failed-scenarios.html");
        } catch (IOException e) {
            System.err.println("❌ Error writing failed scenario report: " + e.getMessage());
        }

        return totalFailures;
    }
}