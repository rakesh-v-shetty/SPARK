import java.io.IOException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class FossilFuelDependencyReducer extends Reducer<Text, Text, Text, Text> {
    
    @Override
    public void reduce(Text key, Iterable<Text> values, Context context) 
            throws IOException, InterruptedException {
        
        double totalBrownCoal = 0.0;
        double totalCoalGas = 0.0;
        double totalNaturalGas = 0.0;
        double totalHardCoal = 0.0;
        double totalOil = 0.0;
        double totalOilShale = 0.0;
        double totalPeat = 0.0;
        double totalFossil = 0.0;
        double totalGeneration = 0.0;
        double totalLoad = 0.0;
        int count = 0;
        
        for (Text value : values) {
            String[] parts = value.toString().split(",");
            totalBrownCoal += Double.parseDouble(parts[0]);
            totalCoalGas += Double.parseDouble(parts[1]);
            totalNaturalGas += Double.parseDouble(parts[2]);
            totalHardCoal += Double.parseDouble(parts[3]);
            totalOil += Double.parseDouble(parts[4]);
            totalOilShale += Double.parseDouble(parts[5]);
            totalPeat += Double.parseDouble(parts[6]);
            totalFossil += Double.parseDouble(parts[7]);
            totalGeneration += Double.parseDouble(parts[8]);
            totalLoad += Double.parseDouble(parts[9]);
            count++;
        }
        
        // Calculate averages
        double avgBrownCoal = totalBrownCoal / count;
        double avgCoalGas = totalCoalGas / count;
        double avgNaturalGas = totalNaturalGas / count;
        double avgHardCoal = totalHardCoal / count;
        double avgOil = totalOil / count;
        double avgOilShale = totalOilShale / count;
        double avgPeat = totalPeat / count;
        double avgTotalFossil = totalFossil / count;
        double avgTotalGeneration = totalGeneration / count;
        double avgLoad = totalLoad / count;
        
        // Calculate dependency percentages
        double fossilDependencyPercent = avgTotalGeneration > 0 ? (avgTotalFossil / avgTotalGeneration) * 100 : 0;
        
        // Calculate composition of fossil fuels
        double brownCoalPercent = avgTotalFossil > 0 ? (avgBrownCoal / avgTotalFossil) * 100 : 0;
        double coalGasPercent = avgTotalFossil > 0 ? (avgCoalGas / avgTotalFossil) * 100 : 0;
        double naturalGasPercent = avgTotalFossil > 0 ? (avgNaturalGas / avgTotalFossil) * 100 : 0;
        double hardCoalPercent = avgTotalFossil > 0 ? (avgHardCoal / avgTotalFossil) * 100 : 0;
        double oilPercent = avgTotalFossil > 0 ? (avgOil / avgTotalFossil) * 100 : 0;
        double oilShalePercent = avgTotalFossil > 0 ? (avgOilShale / avgTotalFossil) * 100 : 0;
        double peatPercent = avgTotalFossil > 0 ? (avgPeat / avgTotalFossil) * 100 : 0;
        
        String result = String.format("%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%d", 
            avgLoad, avgTotalFossil, avgTotalGeneration, fossilDependencyPercent,
            avgBrownCoal, avgCoalGas, avgNaturalGas, avgHardCoal, avgOil, avgOilShale, avgPeat,
            brownCoalPercent, coalGasPercent, naturalGasPercent, hardCoalPercent, oilPercent, count);
        
        context.write(key, new Text(result));
    }
}