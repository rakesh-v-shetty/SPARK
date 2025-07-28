import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class BaseLoadPeakLoadMapper extends Mapper<LongWritable, Text, Text, Text> {
    
    private SimpleDateFormat inputFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
    
    @Override
    public void map(LongWritable key, Text value, Context context) 
            throws IOException, InterruptedException {
        
        String line = value.toString();
        String[] fields = line.split(",");
        
        // Skip header row
        if (fields[0].equals("time")) {
            return;
        }
        
        try {
            // Parse timestamp and extract hour
            Date date = inputFormat.parse(fields[0]);
            Calendar cal = Calendar.getInstance();
            cal.setTime(date);
            int hour = cal.get(Calendar.HOUR_OF_DAY);
            
            // Classify as base load (22:00-06:00) or peak load (07:00-21:00)
            String loadType = "";
            if (hour >= 22 || hour <= 6) {
                loadType = "BASE_LOAD";
            } else {
                loadType = "PEAK_LOAD";
            }
            
            // Get actual load
            double actualLoad = parseDouble(fields[24]); // total load actual
            
            // Calculate generation from each source
            double nuclear = parseDouble(fields[14]);
            double hydro = parseDouble(fields[11]) + parseDouble(fields[12]);
            double coal = parseDouble(fields[2]) + parseDouble(fields[5]);
            double gas = parseDouble(fields[3]) + parseDouble(fields[4]);
            double renewable = parseDouble(fields[9]) + parseDouble(fields[16]) + 
                             parseDouble(fields[17]) + parseDouble(fields[19]) + parseDouble(fields[20]);
            double oil = parseDouble(fields[6]) + parseDouble(fields[7]);
            double other = parseDouble(fields[15]) + parseDouble(fields[18]);
            
            // Create output value with all generation sources
            String outputValue = String.format("%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f", 
                actualLoad, nuclear, hydro, coal, gas, renewable, oil, other);
            
            context.write(new Text(loadType), new Text(outputValue));
            
        } catch (ParseException e) {
            // Skip malformed records
            return;
        }
    }
    
    private double parseDouble(String value) {
        try {
            return value.isEmpty() ? 0.0 : Double.parseDouble(value);
        } catch (NumberFormatException e) {
            return 0.0;
        }
    }
}