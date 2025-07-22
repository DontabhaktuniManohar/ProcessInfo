package ReqRes;

import com.intuit.karate.Results;
import com.intuit.karate.Runner;
import com.intuit.karate.core.FeatureResult;

import java.util.List;
import java.util.stream.Collectors;

public class KarateParallelTest {

    public static void main(String[] args) {
        Results results = Runner.path("classpath:*")
                .parallel(5);

        List<FeatureResult> featureResults = results.getFeatureResults().collect(Collectors.toList());

        for (FeatureResult fr : featureResults) {
            // Use toString() since getPath()/getRelativePath() are unavailable in 1.4.1
            String fullPath = fr.getFeature().getResource().toString(); // e.g., "classpath:ReqRes/sample.feature"
            String featureName = fullPath.replace("classpath:", "");    // clean it up

            int failed = fr.getFailedCount();
            int total = fr.getScenarioCount();
            int passed = total - failed;

            // Push metrics (you must create this class separately)
            KarateMetricsPusher.pushFeatureMetrics(featureName, total, passed, failed);
        }

        if (results.getFailCount() > 0) {
            System.exit(1); // Fail build if any scenario fails
        }
    }
}
