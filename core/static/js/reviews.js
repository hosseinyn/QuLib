const ctxProgress = document.getElementById('studentProgressChart').getContext('2d');

const studentProgressChart = new Chart(ctxProgress, {
    type: 'line',
    data: {
        labels: [
            'مهر', 'آبان', 'آذر', 'دی',
            'بهمن', 'اسفند', 'فروردین',
            'اردیبهشت', 'خرداد'
        ],
        datasets: [
            {
                label: 'میزان علاقه به کتاب‌های کمک‌درسی (%)',
                data: [35, 40, 45, 50, 58, 62, 70, 78, 85],
                borderWidth: 3,
                tension: 0.4,
                fill: false,
                yAxisID: 'y-interest'
            },
            {
                label: 'میانگین نمرات دانش‌آموزان',
                data: [12, 12.5, 13, 13.8, 14.5, 15, 15.8, 16.5, 17.2],
                borderWidth: 3,
                tension: 0.4,
                fill: false,
                yAxisID: 'y-score'
            }
        ]
    },
    options: {
        responsive: true,
        interaction: {
            mode: 'index',
            intersect: false
        },
        plugins: {
            title: {
                display: true,
                text: 'روند تأثیر علاقه به کتاب‌های کمک‌درسی بر سطح نمرات مدرسه همکار کولیب',
                font: {
                    family: "tanha, Tahoma, Arial, sans-serif",
                    size: 16,
                    weight: '600'
                }
            },
            legend: {
                labels: {
                    font: {
                        family: "tanha, Tahoma, Arial, sans-serif",
                        size: 13
                    }
                }
            },
            tooltip: {
                rtl: true,
                bodyFont: {
                    family: "tanha, Tahoma, Arial, sans-serif",
                    size: 13
                },
                titleFont: {
                    family: "tanha, Tahoma, Arial, sans-serif",
                    size: 14,
                    weight: '600'
                }
            }
        },
        scales: {
            'y-interest': {
                type: 'linear',
                position: 'right',
                min: 0,
                max: 100,
                title: {
                    display: true,
                    text: 'درصد علاقه',
                    font: {
                        family: "tanha, Tahoma, Arial, sans-serif",
                        size: 14,
                        weight: '500'
                    }
                },
                ticks: {
                    font: {
                        family: "tanha, Tahoma, Arial, sans-serif",
                        size: 12
                    }
                }
            },
            'y-score': {
                type: 'linear',
                position: 'left',
                min: 0,
                max: 20,
                title: {
                    display: true,
                    text: 'میانگین نمره',
                    font: {
                        family: "tanha, Tahoma, Arial, sans-serif",
                        size: 14,
                        weight: '500'
                    }
                },
                ticks: {
                    font: {
                        family: "tanha, Tahoma, Arial, sans-serif",
                        size: 12
                    }
                }
            },
            x: {
                ticks: {
                    font: {
                        family: "tanha, Tahoma, Arial, sans-serif",
                        size: 12
                    }
                }
            }
        }
    }
});

