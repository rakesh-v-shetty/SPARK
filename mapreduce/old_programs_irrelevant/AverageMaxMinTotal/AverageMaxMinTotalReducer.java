import java.io.IOException;

import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class AverageMaxMinTotalReducer extends Reducer<Text, DoubleWritable, Text, Text> {

    @Override
    protected void reduce(Text key, Iterable<DoubleWritable> values, Context context)
            throws IOException, InterruptedException {

        double sum = 0;
        double max = Double.MIN_VALUE;
        double min = Double.MAX_VALUE;
        int count = 0;

        for (DoubleWritable val : values) {
            double v = val.get();
            sum += v;
            count++;
            if (v > max) max = v;
            if (v < min) min = v;
        }

        double average = sum / count;

        context.write(key, new Text("Average = " + average + ", Max = " + max + ", Min = " + min + ", Total = " + sum));

    }
}
