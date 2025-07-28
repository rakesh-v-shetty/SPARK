import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class CompareLoadToGenerationReducer extends Reducer<Text, Text, Text, Text> {

    @Override
    protected void reduce(Text key, Iterable<Text> values, Context context)
            throws IOException, InterruptedException {

        double totalGeneration = 0;
        double totalLoad = 0;

        for (Text val : values) {
            String[] arr = val.toString().split(",");
            totalGeneration += Double.parseDouble(arr[0]);
            totalLoad += Double.parseDouble(arr[1]);
        }

        context.write(key, new Text("Total Generation = " + totalGeneration + ", Total Load = " + totalLoad));

    }
}
