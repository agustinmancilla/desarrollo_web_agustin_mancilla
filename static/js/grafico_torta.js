Highcharts.chart('container_torta', {
    chart: {
        type: 'pie'
    },
    title: {
        text: 'Distribución de Avisos por Tipo de Mascota'
    },
    legend: {
        layout: 'vertical',
        align: 'left',
        verticalAlign: 'middle',
        floating: true,
        borderWidth: 1,
        backgroundColor: Highcharts.defaultOptions.legend.backgroundColor || 'white',
        shadow: true
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    series: [{
        name: 'Cantidad',
        colorByPoint: true,
        data: []
    }]
});
fetch(`${window.location.origin}/estadisticas/grafico_torta`).then((response) => response.json())
    .then((data) => {
        let parsedData = data.map((item) => {
            return {
                name: item.type,
                y: item.count
            };
        });
        Highcharts.chart('container_torta', {
            chart: {
                type: 'pie'
            },
            title: {
                text: 'Distribución de Avisos por Tipo de Mascota'
            },
            series: [{
                name: 'Cantidad',
                colorByPoint: true,
                data: parsedData
            }]
        });
    }).catch((error) => {
        console.error('Error:', error);
    });