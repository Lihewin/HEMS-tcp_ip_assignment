import pywebio
from pyecharts.charts import Bar
from pywebio.output import put_html


def board():
    put_html(
        '''
    <div id="bar" style="width:1000px; height:600px;"></div>
<script src="https://cdn.bootcss.com/jquery/3.0.0/jquery.min.js"></script>
<script type="text/javascript" src="https://assets.pyecharts.org/assets/echarts.min.js"></script>
<script>
    var chart = echarts.init(document.getElementById('bar'), 'white', {renderer: 'canvas'});
    var old_data = [];
    $(
        function () {
            fetchData(chart);
            setInterval(getDynamicData, 2000);
        }
    );

    function fetchData() {
        $.ajax({
            type: "GET",
            url: "http://localhost/pyecharts_backend_bar/lineChart",
            dataType: "json",
            success: function (result) {
                chart.setOption(result);
                old_data = chart.getOption().series[0].data;
            }
        });
    }

    function getDynamicData() {
        $.ajax({
            type: "GET",
            url: "http://localhost/pyecharts_backend_bar/lineDynamicData",
            dataType: "json",
            success: function (result) {
                old_data.push([result.name, result.value]);
                chart.setOption({
                    series: [{data: old_data}]
                });
            }
        });
    }

</script>
    '''
    )
