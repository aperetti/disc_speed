import hvplot.streamz  # noqa
from streamz.dataframe import Random

streaming_df = Random(freq='5ms')

streaming_df.hvplot(backlog=100, height=400, width=500) +\
streaming_df.hvplot.hexbin(x='x', y='z', backlog=2000, height=400, width=500);