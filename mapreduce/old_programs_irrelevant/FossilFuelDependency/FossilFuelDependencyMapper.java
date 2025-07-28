import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class FossilFuelDependencyMapper extends Mapper<LongWritable, Text, Text, Text> {
    
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
            // Parse timestamp and extract season
            Date date = inputFormat.parse(fields[0]);
            Calendar cal = Calendar.getInstance();
            cal.setTime(date);
            int month = cal.get(Calendar.MONTH) + 1; // Calendar.MONTH is 0-based
            
            String season = getSeason(month);
            
            // Get actual load to determine demand level
            double actualLoad = parseDouble(fields[24]); // total load actual
            String demandLevel = getDemandLevel(actualLoad);
            
            // Calculate fossil fuel generation by type
            double brownCoal = parseDouble(fields[2]);  // brown coal/lignite
            double coalGas = parseDouble(fields[3]);    // coal-derived gas
            double naturalGas = parseDouble(fields[4]); // natural gas
            double hardCoal = parseDouble(fields[5]);   // hard coal
            double oil = parseDouble(fields[6]);        // oil
            double oilShale = parseDouble(fields[7]);   // oil shale
            double peat = parseDouble(fields[8]);       // peat
            
            // Calculate total fossil fuel and total generation
            double totalFossil = brownCoal + coalGas + naturalGas + hardCoal + oil + oilShale + peat;
            
            // Calculate total generation (all sources)
            double totalGeneration = totalFossil;
            totalGeneration += parseDouble(fields[1]);  // biomass
            totalGeneration += parseDouble(fields[9]);  // geothermal
            totalGeneration += parseDouble(fields[11]); // hydro run-of-river
            totalGeneration += parseDouble(fields[12]); // hydro water reservoir
            totalGeneration += parseDouble(fields[13]); // marine
            totalGeneration += parseDouble(fields[14]); // nuclear
            totalGeneration += parseDouble(fields[15]); // other
            totalGeneration += parseDouble(fields[16]); // other renewable
            totalGeneration += parseDouble(fields[17]); // solar
            totalGeneration += parseDouble(fields[18]); // waste
            totalGeneration += parseDouble(fields[19]); // wind offshore
            totalGeneration += parseDouble(fields[20]); // wind onshore
            
            // Composite key: season_demandLevel
            String compositeKey = season + "_" + demandLevel;
            
            // Output value: fossil_types,total_fossil,total_generation,actual_load
            String outputValue = String.format("%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f", 
                brownCoal, coalGas, naturalGas, hardCoal, oil, oilShale, peat, 
                totalFossil, totalGeneration, actualLoad);
            
            context.write(new Text(compositeKey), new Text(outputValue));
            
        } catch (ParseException e) {
            // Skip malformed records
            return;
        }
    }
    
    private String getSeason(int month) {
        if (month >= 3 && month <= 5) return "SPRING";
        else if (month >= 6 && month <= 8) return "SUMMER";
        else if (month >= 9 && month <= 11) return "AUTUMN";
        else return "WINTER";
    }
    
    private String getDemandLevel(double load) {
        // You may need to adjust these thresholds based on your data
        if (load < 30000) return "LOW";
        else if (load < 50000) return "MEDIUM";
        else return "HIGH";
    }
    
    private double parseDouble(String value) {
        try {
            return value.isEmpty() ? 0.0 : Double.parseDouble(value);
        } catch (NumberFormatException e) {
            return 0.0;
        }
    }
}