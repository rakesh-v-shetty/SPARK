import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class RenewableFossilRatioMapper extends Mapper<LongWritable, Text, Text, Text> {
    
    private SimpleDateFormat inputFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
    private SimpleDateFormat outputFormat = new SimpleDateFormat("yyyy-MM");
    
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
            // Parse timestamp and extract year-month
            Date date = inputFormat.parse(fields[0]);
            String yearMonth = outputFormat.format(date);
            
            // Calculate renewable energy (indices based on your column order)
            double renewableEnergy = 0.0;
            renewableEnergy += parseDouble(fields[9]);  // generation geothermal
            renewableEnergy += parseDouble(fields[11]); // generation hydro run-of-river
            renewableEnergy += parseDouble(fields[12]); // generation hydro water reservoir
            renewableEnergy += parseDouble(fields[13]); // generation marine
            renewableEnergy += parseDouble(fields[16]); // generation other renewable
            renewableEnergy += parseDouble(fields[17]); // generation solar
            renewableEnergy += parseDouble(fields[19]); // generation wind offshore
            renewableEnergy += parseDouble(fields[20]); // generation wind onshore
            
            // Calculate fossil fuel energy
            double fossilEnergy = 0.0;
            fossilEnergy += parseDouble(fields[2]);  // generation fossil brown coal/lignite
            fossilEnergy += parseDouble(fields[3]);  // generation fossil coal-derived gas
            fossilEnergy += parseDouble(fields[4]);  // generation fossil gas
            fossilEnergy += parseDouble(fields[5]);  // generation fossil hard coal
            fossilEnergy += parseDouble(fields[6]);  // generation fossil oil
            fossilEnergy += parseDouble(fields[7]);  // generation fossil oil shale
            fossilEnergy += parseDouble(fields[8]);  // generation fossil peat
            
            // Emit year-month as key and renewable,fossil as value
            context.write(new Text(yearMonth), new Text(renewableEnergy + "," + fossilEnergy));
            
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