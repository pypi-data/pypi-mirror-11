"""Provide a way to work with pandas data frames in Spark"""
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from sparklingpandas.utils import add_pyspark_path
from functools import reduce

add_pyspark_path()
from sparklingpandas.pstatcounter import PStatCounter


class PRDD:
    """A Pandas Resilient Distributed Dataset (PRDD), is an extension of a
    Spark RDD. You can access the underlying RDD at _rdd, but be
    careful doing so.
    Note: RDDs are lazy, so you operations are not performed until required."""

    def __init__(self, rdd):
        self._rdd = rdd

    @classmethod
    def from_rdd(cls, rdd):
        """Construct a PRDD from an RDD. No checking or validation occurs."""
        return PRDD(rdd)

    def to_spark_sql(self):
        """A Sparkling Pandas specific function to turn a DDF into
        something that Spark SQL can query. To use the result you will
        need to call sqlCtx.inferSchema(rdd) and then register the result
        as a table. Once Spark 1.1 is released this function may be deprecated
        and replacted with to_spark_sql_schema_rdd."""
        raise NotImplementedError("Method deprecated, please use "
                                  "to_spark_sql_schema_rdd instead!")

    def applymap(self, func, **kwargs):
        """Return a new PRDD by applying a function to each element of each
        pandas DataFrame."""
        return self.from_rdd(
            self._rdd.map(lambda data: data.applymap(func), **kwargs))

    def __getitem__(self, key):
        """Returns a new PRDD of elements from that key."""
        return self.from_rdd(self._rdd.map(lambda x: x[key]))

    def groupby(self, *args, **kwargs):
        """Takes the same parameters as groupby on DataFrame.
        Like with groupby on DataFrame disabling sorting will result in an
        even larger performance improvement. This returns a Sparkling Pandas
        L{GroupBy} object which supports many of the same operations as regular
        GroupBy but not all."""
        from sparklingpandas.groupby import GroupBy
        return GroupBy(self._rdd, *args, **kwargs)

    @property
    def dtypes(self):
        """
        Return the dtypes associated with this object
        Uses the types from the first frame.
        """
        return self._rdd.first().dtypes

    @property
    def ftypes(self):
        """
        Return the ftypes associated with this object
        Uses the types from the first frame.
        """
        return self._rdd.first().ftypes

    def get_dtype_counts(self):
        """
        Return the counts of dtypes in this object
        Uses the information from the first frame
        """
        return self._rdd.first().get_dtype_counts()

    def get_ftype_counts(self):
        """
        Return the counts of ftypes in this object
        Uses the information from the first frame
        """
        return self._rdd.first().get_ftype_counts()

    @property
    def axes(self):
        return (self._rdd.map(lambda frame: frame.axes)
                .reduce(lambda xy, ab: [xy[0].append(ab[0]), xy[1]]))

    @property
    def shape(self):
        return (self._rdd.map(lambda frame: frame.shape)
                .reduce(lambda xy, ab: (xy[0] + ab[0], xy[1])))

    def collect(self):
        """Collect the elements in an PRDD and concatenate the partition."""
        # The order of the frame order appends is based on the implementation
        # of reduce which calls our function with
        # f(valueToBeAdded, accumulator) so we do our reduce implementation.
        def append_frames(frame_a, frame_b):
            return frame_a.append(frame_b)
        return self._custom_rdd_reduce(append_frames)

    def _custom_rdd_reduce(self, reduce_func):
        """Provides a custom RDD reduce which preserves ordering if the RDD has
        been sorted. This is useful for us because we need this functionality
        as many pandas operations support sorting the results. The standard
        reduce in PySpark does not have this property.  Note that when PySpark
        no longer does partition reduces locally this code will also need to
        be updated."""
        def accumulating_iter(iterator):
            acc = None
            for obj in iterator:
                if acc is None:
                    acc = obj
                else:
                    acc = reduce_func(acc, obj)
            if acc is not None:
                yield acc
        vals = self._rdd.mapPartitions(accumulating_iter).collect()
        return reduce(accumulating_iter, vals)

    def stats(self, columns):
        """Compute the stats for each column provided in columns.
        Parameters
        ----------
        columns : list of str, contains all columns to compute stats on.
        """
        def reduce_func(sc1, sc2):
            return sc1.merge_pstats(sc2)

        return self._rdd.mapPartitions(lambda partition: [
            PStatCounter(dataframes=partition, columns=columns)])\
            .reduce(reduce_func)
