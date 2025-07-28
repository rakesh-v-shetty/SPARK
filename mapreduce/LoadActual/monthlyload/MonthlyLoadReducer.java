import java.io.IOException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class MonthlyLoadReducer extends Reducer<Text, Text, Text, Text> {
    
    @Override
    public void reduce(Text key, Iterable<Text> values, Context context)
            throws IOException, InterruptedException {
        
        double sum = 0.0;
        
        for (Text value : values) {
            try {
                sum += Double.parseDouble(value.toString());
            } catch (NumberFormatException e) {
                // Skip invalid values
            }
        }
        
        String result = String.format("%.2f", sum);
        context.write(key, new Text(result));
    }
}