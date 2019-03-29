from elasticsearch_dsl import DocType, Text, Boolean, Keyword
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=["120.77.148.37"])


class ES_Doc(DocType):
    type = Text(analyzer='ik_smart')
    # 不索引，节省空间
    path = Keyword()
    downloaded = Boolean()
    # 不索引，节省空间
    filetype = Text(analyzer='english')

    class Meta:
        index = 'emoji'
        doc_type = "emojis"

    class Index:
        name = 'emoji'


if __name__ == "__main__":
    ES_Doc.init()
