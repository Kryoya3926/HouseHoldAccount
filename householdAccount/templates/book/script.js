var COLORS=[
    '#4dc9f6',
    '#f67019',
    '#f53794',
    '#537bc4',
    '#acc236',
    '#166a8f',
    '#00a950',
    '#58595b',
    '#8549ba'
];

var ctx=document.getElementById("myChart-income");
var myLineChart=new Chart(ctx, {
    type: 'pie',
    data: {
        labels: [{% for c in categories_income %}
            '{{c}}',
            {% endfor %}],
        datasets:[
            {
            data:[
                {% for money in money_amount_income %}
                {{money}},
                {% endfor %}
            ],
            backgroundColor: COLORS,
            },
        ],
    },
    options: {
        title: {
            display: true,
            text: '家計簿データ(収入)'
        },
    }
});

var ctx=document.getElementById("myChart-outcome");
var myLineChart=new Chart(ctx, {
    type: 'pie',
    data: {
        labels: [{% for c in categories_outcome %}
            '{{c}}',
            {% endfor %}],
        datasets:[
            {
            data:[
                {% for money in money_amount_outcome %}
                {{money}},
                {% endfor %}
            ],
            backgroundColor: COLORS,
            },
        ],
    },
    options: {
        title: {
            display: true,
            text: '家計簿データ(支出)'
        },
    }
});
