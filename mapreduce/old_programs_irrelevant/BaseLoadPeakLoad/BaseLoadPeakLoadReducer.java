import java.io.IOException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class BaseLoadPeakLoadReducer extends Reducer<Text, Text, Text, Text> {
    
    @Override
    public void reduce(Text key, Iterable<Text> values, Context context) 
            throws IOException, InterruptedException {
        
        double totalLoad = 0.0;
        double totalNuclear = 0.0;
        double totalHydro = 0.0;
        double totalCoal = 0.0;
        double totalGas = 0.0;
        double totalRenewable = 0.0;
        double totalOil = 0.0;
        double totalOther = 0.0;
        int count = 0;
        
        for (Text value : values) {
            String[] parts = value.toString().split(",");
            totalLoad += Double.parseDouble(parts[0]);
            totalNuclear += Double.parseDouble(parts[1]);
            totalHydro += Double.parseDouble(parts[2]);
            totalCoal += Double.parseDouble(parts[3]);
            totalGas += Double.parseDouble(parts[4]);
            totalRenewable += Double.parseDouble(parts[5]);
            totalOil += Double.parseDouble(parts[6]);
            totalOther += Double.parseDouble(parts[7]);
            count++;
        }
        
        // Calculate averages
        double avgLoad = totalLoad / count;
        double avgNuclear = totalNuclear / count;
        double avgHydro = totalHydro / count;
        double avgCoal = totalCoal / count;
        double avgGas = totalGas / count;
        double avgRenewable = totalRenewable / count;
        double avgOil = totalOil / count;
        double avgOther = totalOther / count;
        
        // Calculate total generation
        double totalGeneration = avgNuclear + avgHydro + avgCoal + avgGas + avgRenewable + avgOil + avgOther;
        
        // Calculate percentages
        String result = String.format("%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%d", 
            avgLoad, avgNuclear, avgHydro, avgCoal, avgGas, avgRenewable, avgOil, avgOther,
            totalGeneration > 0 ? (avgNuclear/totalGeneration)*100 : 0,
            totalGeneration > 0 ? (avgHydro/totalGeneration)*100 : 0,
            totalGeneration > 0 ? (avgCoal/totalGeneration)*100 : 0,
            totalGeneration > 0 ? (avgGas/totalGeneration)*100 : 0,
            totalGeneration > 0 ? (avgRenewable/totalGeneration)*100 : 0,
            totalGeneration > 0 ? (avgOil/totalGeneration)*100 : 0,
            count);
        
        context.write(key, new Text(result));
    }
}