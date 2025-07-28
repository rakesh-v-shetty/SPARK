import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.WeekFields;
import java.util.Locale;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class WeeklyEnergyMapper extends Mapper<LongWritable, Text, Text, Text> {
    
    private static final DateTimeFormatter FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ssXXX");
    
    // 0-indexed column positions for renewable energy sources
    private static final int[] RENEWABLE_COLUMNS = {1, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20};
    
    @Override
    public void map(LongWritable key, Text value, Context context) 
            throws IOException, InterruptedException {
        
        String line = value.toString();
        String[] fields = line.split(",");
        
        // Skip header row
        if (fields[0].equals("time") || fields.length < 21) {
            return;
        }
        
        try {
            // Parse timestamp
            String timestamp = fields[0].trim();
            LocalDateTime dateTime = LocalDateTime.parse(timestamp, FORMATTER);
            String weeklyKey = dateTime.getYear() + "-W" + 
                String.format("%02d", dateTime.get(WeekFields.of(Locale.getDefault()).weekOfYear()));
            
            // Create energy values string for the 12 renewable sources
            StringBuilder energyValues = new StringBuilder();
            for (int i = 0; i < RENEWABLE_COLUMNS.length; i++) {
                int columnIndex = RENEWABLE_COLUMNS[i];
                String energyValue = "";
                
                if (columnIndex < fields.length) {
                    energyValue = fields[columnIndex].trim();
                }
                
                if (energyValue.isEmpty() || energyValue.equals("null")) {
                    energyValues.append("0.0");
                } else {
                    try {
                        double energy = Double.parseDouble(energyValue);
                        energyValues.append(String.valueOf(energy));
                    } catch (NumberFormatException e) {
                        energyValues.append("0.0");
                    }
                }
                
                if (i < RENEWABLE_COLUMNS.length - 1) {
                    energyValues.append(",");
                }
            }
            
            context.write(new Text(weeklyKey), new Text(energyValues.toString()));
            
        } catch (Exception e) {
            context.getCounter("ERRORS", "MALFORMED_RECORDS").increment(1);
        }
    }
}