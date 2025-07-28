import java.io.IOException;

import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class AverageMaxMinTotalMapper extends Mapper<LongWritable, Text, Text, DoubleWritable> {

    private Text outKey = new Text();

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

        // Split CSV
        String[] fields = value.toString().split(",");
        // Assuming the CSV structure (with header) includes:
        // 0: time
        // 1: generation biomass
        // 2: generation fossil brown coal
        // 3: generation fossil coal-derived gas
        // 4: generation fossil gas
        // 5: generation fossil hard coal
        // 6: generation fossil oil
        // 7: generation fossil oil shale
        // 8: generation fossil peat
        // 9: generation geothermal
        // 10: generation hydro pumped storage consumption
        // 11: generation hydro run-of-river and poundage
        // 12: generation hydro water reservoir
        // 13: generation marine
        // 14: generation nuclear
        // 15: generation other
        // 16: generation other renewable
        // 17: generation solar
        // 18: generation waste
        // 19: generation wind offshore
        // 20: generation wind onshore

        try {
            double biomass = Double.parseDouble(fields[1]);
            double fossilBrownCoal = Double.parseDouble(fields[2]);
            double fossilCoalDerivedGas = Double.parseDouble(fields[3]);
            double fossilGas = Double.parseDouble(fields[4]);
            double fossilHardCoal = Double.parseDouble(fields[5]);
            double fossilOil = Double.parseDouble(fields[6]);
            double fossilOilShale = Double.parseDouble(fields[7]);
            double fossilPeat = Double.parseDouble(fields[8]);

            double geothermal = Double.parseDouble(fields[9]);

            double hydroPumped = Double.parseDouble(fields[10]);
            double hydroRunning = Double.parseDouble(fields[11]);
            double hydroReservoir = Double.parseDouble(fields[12]);

            double marine = Double.parseDouble(fields[13]);

            double nuclear = Double.parseDouble(fields[14]);

            double other = Double.parseDouble(fields[15]);

            double otherRenewable = Double.parseDouble(fields[16]);

            double solar = Double.parseDouble(fields[17]);

            double waste = Double.parseDouble(fields[18]);

            double windOffshore = Double.parseDouble(fields[19]);

            double windOnshore = Double.parseDouble(fields[20]);

            // Renewable
            outKey.set("Renewable");

            context.write(outKey, new DoubleWritable(
                    biomass + geothermal + hydroPumped + hydroRunning + hydroReservoir + marine + otherRenewable + solar + waste + windOffshore + windOnshore));

            // Fossil
            outKey.set("Fossil");

            context.write(outKey, new DoubleWritable(
                    fossilBrownCoal + fossilCoalDerivedGas + fossilGas + fossilHardCoal + fossilOil + fossilOilShale + fossilPeat));

        } catch (NumberFormatException e) {
            // Handle invalid number format gracefully
        }
    }
}
