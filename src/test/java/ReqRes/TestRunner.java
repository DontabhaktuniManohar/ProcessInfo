package ReqRes;

import com.intuit.karate.junit5.Karate;

public class TestRunner {

    @Karate.Test
    Karate testReqres() {
        return Karate.run("Reqres").relativeTo(getClass());
    }
}
