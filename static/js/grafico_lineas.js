Highcharts.chart('container_lineas', {
    chart: {
        type: 'line'
    },
    title: {
        text: 'Número de avisos por día'
    },
    xAxis: {
        type: 'datetime',
        dateTimeLabelFormats: {
            month: '%b %e, %Y'
        },
        title: {
            text: 'Fecha'
        }
    },
    yAxis: {
        title: {
            text: 'Número de avisos'
        }
    },
    legend: {
        align: 'left',
        verticalAlign: 'top',
        borderWidth: 0,
    },
    tooltip: {
        shared: true,
        crosshairs: true
    },
    series: [{
        name: 'Avisos',
        data: [],
        linewidth: 1,
        marker: {
            enabled: true,
            radius: 3
        },
        color: '#7cb5ec'
    }],
    noData: {
        style: {
            fontWeight: 'bold',
            fontSize: '15px',
            color: '#303030'
        }
    }
});
fetch(`${window.location.origin}/estadisticas/grafico_lineas`).then((response) => response.json())
    .then((data) => {
        let parsedData = data.map((item) => {
            const [year, month, day] = item.date.split('-').map((part) => parseInt(part, 10));
            return [
                Date.UTC(year, month - 1, day), 
                item.count
            ];
        });

        const chart = Highcharts.charts.find(
            (chart) =>chart && chart.renderTo.id === 'container_lineas'
        );

        chart.update({
            series: [{
                data: parsedData
            },
        ],
    });
}).catch((error) => console.error('Error:', error));
    