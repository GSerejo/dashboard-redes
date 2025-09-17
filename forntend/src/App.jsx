import React, {useEffect, useState} from 'react'
import { Bar } from 'react-chartjs-2'
import { Chart, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'


Chart.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)


export default function App(){
const [latest, setLatest] = useState(null)
const [history, setHistory] = useState([])


useEffect(()=>{
const iv = setInterval(()=>{
fetch('/api/windows/latest').then(r=>r.json()).then(setLatest).catch(()=>{})
fetch('/api/windows/history?n=12').then(r=>r.json()).then(setHistory).catch(()=>{})
},2000)
return ()=> clearInterval(iv)
},[])


const handleBarClick = (evt, elements) =>{
if(!elements.length) return
const idx = elements[0].index
const labels = Object.keys(latest.clients)
const client = labels[idx]
fetch(`/api/drilldown?start=${latest.start}&client=${client}`).then(r=>r.json()).then(data=>{
// simples modal com alert; trocar por modal bonito
alert(JSON.stringify(data.protocols))
})
}


if(!latest) return <div style={{padding:20}}>Carregando...</div>


const labels = Object.keys(latest.clients)
const inData = labels.map(ip=> latest.clients[ip].in)
const outData = labels.map(ip=> latest.clients[ip].out)


const data = {
labels,
datasets:[
{ label: 'In', data: inData, stack: 'stack1' },
{ label: 'Out', data: outData, stack: 'stack1' }
]
}


const options = {
onClick: (evt, items) => handleBarClick(evt, items),
plugins: { tooltip: { mode: 'index' } },
responsive: true,
scales: { x: { stacked: true }, y: { stacked: true } }
}


return (
<div style={{padding:20}}>
<h2>Dashboard Tráfego — janela {new Date(latest.start*1000).toLocaleTimeString()}</h2>
<div style={{width:'90%', maxWidth:1200}}>
<Bar data={data} options={options} />
</div>
</div>
)
}