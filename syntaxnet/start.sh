#nohup bazel-bin/syntaxnet/tokenizer_server --alsologtostderr > tokenizer_server.log &
#nohup bazel-bin/syntaxnet/morpher_server --alsologtostderr > morpher_server.log &
#nohup bazel-bin/syntaxnet/tagger_server --alsologtostderr > tagger_server.log &
#nohup bazel-bin/syntaxnet/parser_server --alsologtostderr > parser_server.log &
nohup bazel-bin/syntaxnet/brain_pos_server --alsologtostderr > brain_pos_server.log &
nohup python demo_server.py > demo_server.log &

