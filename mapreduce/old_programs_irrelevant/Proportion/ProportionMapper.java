import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.mapreduce.Mapper;

public class ProportionMapper extends Mapper<LongWritable, Text, Text, Text> {

    private Text outKey = new Text();

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

        String[] fields = value.toString().split(",");
        // 0: time
        // 1-20: generation by energy sources
        try {
            double total = 0;

            for (int i = 1; i <= 20; i++) {
                total += Double.parseDouble(fields[i]);
            }

            // extract week or year
            String datetime = fields[0].split(" ")[0];
            // you can extract the year
            String year = datetime.split("-")[0];
            // or by week number if needed
            // here we use year:
            outKey.set(year);

            // construct a CSV-like: "fossilBrownCoal=..., solar=..., total=..."
            StringBuilder sb = new StringBuilder();

            sb.append("fossilBrownCoal=").append(fields[2])
              .append(",fossilCoalDerivedGas=").append(fields[3])
              .append(",fossilGas=").append(fields[4])
              .append(",fossilHardCoal=").append(fields[5]) 
              .append(",fossilOil=").append(fields[6]) 
              .append(",fossilOilShale=").append(fields[7]) 
              .append(",fossilPeat=").append(fields[8]) 
              .append(",geothermal=").append(fields[9]) 
              .append(",hydroPumped=").append(fields[10]) 
              .append(",hydroRunning=").append(fields[11]) 
              .append(",hydroReservoir=").append(fields[12]) 
              .append(",marine=").append(fields[13]) 
              .append(",nuclear=").append(fields[14]) 
              .append(",other=").append(fields[15]) 
              .append(",otherRenewable=").append(fields[16]) 
              .append(",solar=").append(fields[17]) 
              .append(",waste=").append(fields[18]) 
              .append(",windOffshore=").append(fields[19]) 
              .append(",windOnshore=").append(fields[20]) 
              .append(",total=").append(total);

            context.write(outKey, new Text(sb.toString()));

        } catch (NumberFormatException e) {
            // Handle gracefully
        }
    }
}
