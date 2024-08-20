

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Optional;

public class ProcessInfo {

    public static void main(String[] args) {
        try {
            // Command to execute on Linux
            String command = "ps -eo pid,comm";

            // Initialize the process builder
            ProcessBuilder processBuilder = new ProcessBuilder();
            processBuilder.command("bash", "-c", command);

            // Start the process
            Process process = processBuilder.start();

            // Get the PID of the process
            long pid = process.pid();
            System.out.println("Process ID: " + pid);

            // Read the output of the command
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }

            // Wait for the process to finish
            int exitCode = process.waitFor();
            System.out.println("Exited with code: " + exitCode);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
