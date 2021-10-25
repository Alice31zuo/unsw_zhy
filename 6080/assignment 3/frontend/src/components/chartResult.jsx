import React from 'react'
import { Bar, Radar, Scatter } from 'react-chartjs-2';
import '../css/result.css'

const ResultChart = () => {
  // these are three chart to show the top five score and rate of person and quesitons ,and the right rate of each quesiton
  const numberPlay = 5
  const label = Array.from({ length: numberPlay }, (item, index) => `player ${index + 1}`)
  const background = new Array(numberPlay).fill('rgba(255, 99, 132, 0.3)')
  const backgroundboard = new Array(numberPlay).fill('rgba(255, 99, 132, 1)')
  let datacontent = []
  datacontent = new Array(numberPlay).fill(0)
  for (let i = 0; i < numberPlay; i += 1) {
    datacontent[i] = Math.ceil(Math.random() * 100)
  }
  const data = {
    labels: label,
    datasets: [
      {
        label: 'top five score',
        data: datacontent,
        backgroundColor: background,
        borderColor: backgroundboard,
        borderWidth: 1,
      },
    ],
  };
  const options = {
    scales: {
      yAxes: [
        {
          ticks: {
            beginAtZero: true,
          },
        },
      ],
    },
  };

  const numberPlayall = 10
  let datax = []
  datax = new Array(numberPlayall).fill(0)
  for (let i = 0; i < numberPlayall; i += 1) {
    datax[i] = Math.ceil(Math.random() * 100)
  }
  let datay = []
  datay = new Array(numberPlayall).fill(0)
  for (let i = 0; i < numberPlayall; i += 1) {
    datay[i] = Math.ceil(Math.random() * 100)
  }
  let datause = ['0']
  datause = []
  for (let i = 0; i < numberPlayall; i += 1) {
    datause.push({ x: datax[i], y: datay[i] })
  }
  const datathree = {
    datasets: [
      {
        label: 'right rate of people and question',
        data: datause,
        backgroundColor: 'rgba(205, 109, 12, 1)',
      },
    ],
  };

  const optionsthree = {
    scales: {
      yAxes: [
        {
          ticks: {
            beginAtZero: true,
          },
        },
      ],
      xAxes: [
        {
          ticks: {
            beginAtZero: true,
          },
        },
      ],
    },
  };

  const numberQuestion = 10
  const labeltwo = Array.from({ length: numberQuestion }, (item, index) => `question ${index + 1}`)
  let datacontenttwo = []
  datacontenttwo = new Array(numberQuestion).fill(0)
  for (let i = 0; i < numberQuestion; i += 1) {
    datacontenttwo[i] = Math.ceil(Math.random() * 100)
  }

  const datatwo = {
    labels: labeltwo,
    datasets: [
      {
        label: 'right rate of every question (%)',
        data: datacontenttwo,
        backgroundColor: 'rgba(25, 99, 199, 0.2)',
        borderColor: 'rgba(25, 99, 188, 1)',
        borderWidth: 1,
      },
    ],
  };
  const optionstwo = {
    scale: {
      ticks: { beginAtZero: true },
    },
  };

  return (
    <div className = 'resultContainer'>
      <div className = 'resultArea'>
        <div><h1 className = 'resultword'>you did it ! these are results </h1></div>
        <div className = 'charcontainer'>
          <Bar data = {data} options = {options} />
        </div>
        <br/>
        <br/>
        <div>
          <Scatter data = {datathree} options = {optionsthree}/>
        </div>
        <br/>
        <br/>
        <div className = 'charcontainer'>
          <Radar data = {datatwo} options = {optionstwo} />
        </div>
      </div>
    </div>
  )
}

export default ResultChart;
