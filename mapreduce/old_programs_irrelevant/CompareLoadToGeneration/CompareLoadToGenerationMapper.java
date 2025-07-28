import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.mapreduce.Mapper;

public class CompareLoadToGenerationMapper extends Mapper<LongWritable, Text, Text, Text> {

    private Text outKey = new Text();

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

        String[] fields = value.toString().split(",");
        // 0: time
        // total load forecast: 21
        // total load actual: 22
        try {
            double total = 0;

            for (int i = 1; i <= 20; i++) {
                total += Double.parseDouble(fields[i]);
            }

            double load = Double.parseDouble(fields[21]);

            // day
            String datetime = fields[0];
            String day = datetime.split(" ")[0];
            outKey.set(day);

            context.write(outKey, new Text(total + "," + load));

        } catch (NumberFormatException e) {
            // Handle gracefully
        }
    }
}
