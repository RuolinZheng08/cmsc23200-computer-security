#!/bin/sh
IFS='' read -r -d '' var << 'EOF'
                    ���JA�4�h�8�a~�p�^��M+=�9b"�T���̦�jg�s�epB'��5,�}�MaL����_���|C�1-����9#?zE�l��@�� @�_h��K��G"��<�; ��� |E�S��%v�%ff
EOF
IFS='' read -r -d '' bool << 'EOF'
                    ���JA�4�h�8�a~�p�^��M+=�9b"�T���̦�jg�s�epB'��5,�}�MaL����_���|C�1-����9#?zE�l��@�� @�_h��K��G"��<�; ��� |E�S��%v�%ff
EOF
if [ "$var" == "$bool" ]
then
	echo "my name is ruolinzheng, and i am good";
else
	echo "my name is ruolinzheng, and i am evil";
fi