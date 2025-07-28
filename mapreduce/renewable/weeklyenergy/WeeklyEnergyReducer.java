import java.io.IOException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class WeeklyEnergyReducer extends Reducer<Text, Text, Text, Text> {
    
    private static final int NUM_RENEWABLE_SOURCES = 12;
    
    @Override
    public void reduce(Text key, Iterable<Text> values, Context context)
            throws IOException, InterruptedException {
        
        double[] sums = new double[NUM_RENEWABLE_SOURCES];
        
        for (Text value : values) {
            String[] energyValues = value.toString().split(",");
            for (int i = 0; i < energyValues.length && i < NUM_RENEWABLE_SOURCES; i++) {
                try {
                    sums[i] += Double.parseDouble(energyValues[i]);
                } catch (NumberFormatException e) {
                    // Skip invalid values
                }
            }
        }
        
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < NUM_RENEWABLE_SOURCES; i++) {
            result.append(String.format("%.2f", sums[i]));
            if (i < NUM_RENEWABLE_SOURCES - 1) {
                result.append(",");
            }
        }
        
        context.write(key, new Text(result.toString()));
    }
}