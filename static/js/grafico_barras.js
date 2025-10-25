Highcharts.chart('container_barras', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Adopciones por Tipo y Mes'
    },
    xAxis: {
        categories: [],
        title: { 
            text: 'Mes'
        }
    },
    yAxis: {
        title: {
            text: 'Cantidad de Adopciones'
        }
    },
    legend: {
        align: 'center',
        verticalAlign: 'bottom',
        borderWidth: 0
    },
    tooltip: {
        shared: true,
        crosshairs: true
    },
    plotOptions: {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        }
    },
    series: [],
    credits: {
        enabled: false
    }
});
fetch(`${window.location.origin}/estadisticas/grafico_barras`).then((response) => response.json())
    .then((data) => {
        const nombresmeses= {1 : 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'};
        const meses = data.meses.map(mes => nombresmeses[mes] || mes);
        const series = data.series;
        Highcharts.chart('container_barras', {
            chart: {
                type: 'column'
            },
            title: {
                text: 'Cantidad de Adopciones por Tipo para cada Mes'
            },
            xAxis: {
                categories: meses
            },
            yAxis: {
                title: {
                    text: 'Cantidad de Adopciones'
                }
            },
            series: series
        });
    }).catch((error) => {
        console.error('Error:', error);
});