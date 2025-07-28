import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class DailyLoadMapper extends Mapper<LongWritable, Text, Text, Text> {
    
    private static final DateTimeFormatter FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ssXXX");
    
    // 0-indexed column position for total load actual (24th column)
    private static final int LOAD_ACTUAL_COLUMN = 23;
    
    @Override
    public void map(LongWritable key, Text value, Context context) 
            throws IOException, InterruptedException {
        
        String line = value.toString();
        String[] fields = line.split(",");
        
        // Skip header row
        if (fields[0].equals("time") || fields.length < 25) {
            return;
        }
        
        try {
            // Parse timestamp
            String timestamp = fields[0].trim();
            LocalDateTime dateTime = LocalDateTime.parse(timestamp, FORMATTER);
            String dailyKey = dateTime.toLocalDate().toString();
            
            // Get load actual value from column 24
            String loadValue = "";
            if (LOAD_ACTUAL_COLUMN < fields.length) {
                loadValue = fields[LOAD_ACTUAL_COLUMN].trim();
            }
            
            if (loadValue.isEmpty() || loadValue.equals("null")) {
                loadValue = "0.0";
            } else {
                try {
                    double load = Double.parseDouble(loadValue);
                    loadValue = String.valueOf(load);
                } catch (NumberFormatException e) {
                    loadValue = "0.0";
                }
            }
            
            context.write(new Text(dailyKey), new Text(loadValue));
            
        } catch (Exception e) {
            context.getCounter("ERRORS", "MALFORMED_RECORDS").increment(1);
        }
    }
}