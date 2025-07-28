import java.io.IOException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class RenewableFossilRatioReducer extends Reducer<Text, Text, Text, Text> {
    
    @Override
    public void reduce(Text key, Iterable<Text> values, Context context) 
            throws IOException, InterruptedException {
        
        double totalRenewable = 0.0;
        double totalFossil = 0.0;
        int count = 0;
        
        for (Text value : values) {
            String[] parts = value.toString().split(",");
            totalRenewable += Double.parseDouble(parts[0]);
            totalFossil += Double.parseDouble(parts[1]);
            count++;
        }
        
        double totalEnergy = totalRenewable + totalFossil;
        double renewableRatio = totalEnergy > 0 ? (totalRenewable / totalEnergy) * 100 : 0.0;
        double fossilRatio = totalEnergy > 0 ? (totalFossil / totalEnergy) * 100 : 0.0;
        
        String result = String.format("%.2f,%.2f,%.2f,%.2f,%d", 
            totalRenewable, totalFossil, renewableRatio, fossilRatio, count);
        
        context.write(key, new Text(result));
    }
}