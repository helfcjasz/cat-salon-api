import Header from './components/Header.jsx';
import VisitTable from './components/VisitTable.jsx';
import { useState } from 'react';
import VisitForm from './components/VisitForm.jsx';
import './css/style.css';
import Footer from './components/Footer.jsx'
import Links from './components/Links.jsx'
import About from './components/About.jsx';
import Info from './components/Info.jsx';


const initialVisits = [
  { id: 1, catName: 'Ніка', catBreed: 'сіамська кішка', serviceType: 'Вичісування',
    serviceDate: '2026-11-06', serviceTime: '12:00', catMass: 5.5, agr_confirmation: false },
  { id: 2, catName: 'Мія', catBreed: 'метис', serviceType: 'Купання та сушіння',
    serviceDate: '2026-11-03', serviceTime: '13:00', catMass: 3.4, agr_confirmation: true },
  { id: 3, catName: 'Люся', catBreed: 'сибірська', serviceType: 'Вичісування',
    serviceDate: '2026-11-01', serviceTime: '10:00', catMass: 3.1, agr_confirmation: true },
  { id: 4, catName: 'Йосип', catBreed: 'метис', serviceType: 'Догляд за кігтиками та вушками',
    serviceDate: '2026-11-05', serviceTime: '11:00', catMass: 5.2, agr_confirmation: true },
  { id: 5, catName: 'Марсік', catBreed: 'британський короткошерстий', serviceType: 'Гігієнічна стрижка',
    serviceDate: '2026-11-20', serviceTime: '15:00', catMass: 4.8, agr_confirmation: true }
];



function App() {
  const [visits, setVisits] = useState(initialVisits);


  function addVisit(visit) {
    const newVisit = {
      ...visit,
      id: Date.now(),
      catMass: Number(visit.catMass)
    };
    setVisits([...visits, newVisit]);
  }


  function deleteVisit(id) {
    setVisits(visits.filter(visit => visit.id !== id));
  }

  


  return (
    <>{}
    <Header />
    
    <div className="container">
      <About />
      <Info />
      {visits.length === 0 ? <h2 className = "section section-title empty-table" >Записів немає</h2> : <VisitTable visits={visits} onDelete={deleteVisit} />}
      <VisitForm onAdd={addVisit} visits={visits}/>
      <Links />  
    </div>

    <Footer />

    </>
  );
}

export default App;
