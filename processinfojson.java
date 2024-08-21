package com.pidinfo.demo;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;

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

            // Read the output of the command
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;

            // Skip the header line
            reader.readLine();

            JSONArray processList = new JSONArray();
            while ((line = reader.readLine()) != null) {
                String[] parts = line.trim().split("\\s+", 2);
                if (parts.length == 2) {
                    JSONObject processInfo = new JSONObject();
                    processInfo.put("pid", Integer.parseInt(parts[0]));
                    processInfo.put("command", parts[1]);
                    processList.put(processInfo);
                }
            }

            // Create the JSON output
            JSONObject output = new JSONObject();
            output.put("processId", pid);
            output.put("processList", processList);

            // Print the JSON output
            System.out.println(output.toString(2));  // Pretty print with indentation

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
