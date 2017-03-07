from flask import Flask
from flask import request
from sklearn import linear_model
from flask.ext.cors import CORS

reg = linear_model.LinearRegression()
file = open("traffic.txt", "r")

datalist = [];
statuslist = [];
for line in file:
    if len(line) != '':
        line = line.split(' ')
        temp = line[0].split(',')
        templist = []
        for i in temp:
            templist.append(int(i))
        statuslist.append(int(line[1]))
        datalist.append(templist)

reg.fit(datalist,statuslist)
file.close()


app = Flask(__name__)
CORS(app)


@app.route('/post', methods=['POST'])
def hello_world():
    name = request.args.get('name')
    direction = request.args.get('direction')
    day = request.args.get('day')
    time = request.args.get('time')
    status = request.args.get('status')

    file = open('traffic.txt', "a")
    file.write("\n" + name + "," + direction + "," + day +  "," + time + " " + status);
    file.close()

    file = open("traffic.txt", "r")

    datalist = [];
    statuslist = [];
    for line in file:
        if len(line) != '':
            line = line.split(' ')
            temp = line[0].split(',')
            templist = []
            for i in temp:
                templist.append(int(i))
            statuslist.append(int(line[1]))
            datalist.append(templist)

    reg.fit(datalist,statuslist)
    file.close()

    return 'ok'

@app.route('/getstatus', methods=['GET'])
def get_status():
    list = []
    list.append(int(request.args.get('name')))
    list.append(int(request.args.get('direction')))
    list.append(int(request.args.get('day')))
    list.append(int(request.args.get('time')))

    valuepredict = [];
    valuepredict.append(list);

    return str(int(reg.predict(valuepredict)[0]))


if __name__ == '__main__':
    app.run(host='0.0.0.0')