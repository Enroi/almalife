FROM apache/spark:4.2.0-scala2.13-java25-python3-r-ubuntu

USER root

ENV PATH                $PATH:$SPARK_HOME/bin

ENV HADOOP_VERSION      3.4.2
ENV HADOOP_HOME         /opt/hadoop

ADD hadoop-$HADOOP_VERSION.tar.gz /opt
RUN mv /opt/hadoop-$HADOOP_VERSION $HADOOP_HOME && ln -s $HADOOP_HOME/lib/native/*.so /usr/lib64/

USER spark

RUN wget -P /opt/spark/jars https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.10/postgresql-42.7.10.jar

COPY spark-defaults.conf /opt/spark/conf/spark-defaults.conf
