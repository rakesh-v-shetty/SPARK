import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class ProportionReducer extends Reducer<Text, Text, Text, Text> {

    @Override
    protected void reduce(Text key, Iterable<Text> values, Context context)
            throws IOException, InterruptedException {

        double total = 0;

        double fossilBrownCoal = 0;
        double fossilCoalDerived = 0;
        double fossilGas = 0;
        double fossilHardCoal = 0;
        double fossilOil = 0;
        double fossilOilShale = 0;
        double fossilPeat = 0;

        double geothermal = 0;

        double hydroPumped = 0;
        double hydroRunning = 0;
        double hydroReservoir = 0;

        double marine = 0;

        double nuclear = 0;

        double other = 0;

        double otherRenewable = 0;

        double solar = 0;

        double waste = 0;

        double windOffshore = 0;

        double windOnshore = 0;

        for (Text val : values) {
            String[] arr = val.toString().split(",");
            for (String item : arr) {
                String[] pair = item.split("=");
                if (pair.length == 2) {
                    String k = pair[0].trim();
                    double v = Double.parseDouble(pair[1]);

                    if (k.equals("fossilBrownCoal")) fossilBrownCoal += v;
                    else if (k.equals("fossilCoalDerivedGas")) fossilCoalDerived += v;
                    else if (k.equals("fossilGas")) fossilGas += v;
                    else if (k.equals("fossilHardCoal")) fossilHardCoal += v;
                    else if (k.equals("fossilOil")) fossilOil += v;
                    else if (k.equals("fossilOilShale")) fossilOilShale += v;
                    else if (k.equals("fossilPeat")) fossilPeat += v;

                    else if (k.equals("geothermal")) geothermal += v;

                    else if (k.equals("hydroPumped")) hydroPumped += v;
                    else if (k.equals("hydroRunning")) hydroRunning += v;
                    else if (k.equals("hydroReservoir")) hydroReservoir += v;

                    else if (k.equals("marine")) marine += v;

                    else if (k.equals("nuclear")) nuclear += v;

                    else if (k.equals("other")) other += v;

                    else if (k.equals("otherRenewable")) otherRenewable += v;

                    else if (k.equals("solar")) solar += v;

                    else if (k.equals("waste")) waste += v;

                    else if (k.equals("windOffshore")) windOffshore += v;

                    else if (k.equals("windOnshore")) windOnshore += v;

                    else if (k.equals("total")) total += v;

                }
            }
        }

        context.write(key, new Text(
                String.format("fossilBrownCoal=%.2f, fossilCoalDerived=%.2f, fossilGas=%.2f, fossilHardCoal=%.2f, fossilOil=%.2f, fossilOilShale=%.2f, fossilPeat=%.2f, geothermal=%.2f, hydroPumped=%.2f, hydroRunning=%.2f, hydroReservoir=%.2f, marine=%.2f, nuclear=%.2f, other=%.2f, otherRenewable=%.2f, solar=%.2f, waste=%.2f, windOffshore=%.2f, windOnshore=%.2f, total=%.2f",
                        fossilBrownCoal, fossilCoalDerived, fossilGas, fossilHardCoal, fossilOil, fossilOilShale, fossilPeat, geothermal, hydroPumped, hydroRunning, hydroReservoir, marine, nuclear, other, otherRenewable, solar, waste, windOffshore, windOnshore, total)));
    }
}
