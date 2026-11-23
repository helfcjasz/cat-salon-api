import { useState } from 'react';

const emptyForm = {
  catName: '', catBreed: '', serviceType: '',
  serviceDate: '', serviceTime: '', catMass: '', agr_confirmation: false
};



function VisitForm({ onAdd, visits}) {
    const [form, setForm] = useState(emptyForm);
    const [error, setError] = useState('');

    function handleChange(event) {
        const { name, value, type, checked } = event.target;
        setForm({ ...form, [name]: type === 'checkbox' ? checked : value });
    }

    function handleSubmit(event) {
        event.preventDefault();
        if (form.catName.trim() === '') {
            setError('Вкажіть кличку котика');
            return;
        }

        if (form.serviceDate === '') {
            setError('Вкажіть дату запису');
            return;
        }


        const appointmentsOnDate = visits.filter(v => v.serviceDate === form.serviceDate);

        if (appointmentsOnDate.length >= 6) {
            setError('На цю дату вже немає вільних місць. Виберіть інший день.');
            return;
        }



        if (form.serviceTime === '' || form.serviceTime < '10:00' || form.serviceTime > '16:00') {
            setError('Оберіть час візиту в межах робочих годин (10:00 - 16:00)');
            return;
        }

        const isTimeTaken = appointmentsOnDate.some(v => v.serviceTime === form.serviceTime);

        if (isTimeTaken) {
            setError(`На ${form.serviceTime} у цей день вже є запис. Виберіть інший час.`);
            return;
        }

        const mass = Number(form.catMass);
        if (mass < 1 || mass > 20) {
            setError('Маса кота має бути від 1 до 20 кг');
            return;
        }

        if (!form.serviceTime.endsWith(':00')) {
            setError('Запис можливий лише на рівну годину');
            return;
        }

        const today = new Date().toISOString().split('T')[0];

        if (form.serviceDate <= today) {
            setError('Цей час вже минув. Оберіть майбутню дату та годину.');
            return;
        }


        setError('');



        onAdd(form);
        setForm(emptyForm);
    }

    const today = new Date().toISOString().split('T')[0];
    
    return (
        <section className="section">
        <h2 className="section-title">Записатися на грумінг</h2>
            <form className="form" onSubmit= {handleSubmit} >
                <div className="form-grid">

                    <div className="form-field">
                        <label htmlFor="catName" className="form-label">Кличка</label>
                        <input className= "form-input" type="text" id="catName" name="catName" placeholder="Введіть кличку..." value={form.catName} onChange={handleChange} />
                    </div>

                    <div className="form-field">
                        <label className="form-label" htmlFor="catBreed">Порода</label>
                        <input className= "form-input" type="text" id="catBreed" name="catBreed" placeholder="Введіть породу..." value={form.catBreed} onChange={handleChange}/>
                    </div>

                    <div className="form-field">
                        <label className="form-label" htmlFor="serviceType">Послуга</label>
                        <select className= "form-input" id="serviceType" name="serviceType" value={form.serviceType} onChange={handleChange}> 
                            <option>Купання та сушіння</option>
                            <option>Вичісування</option>
                            <option>Гігієнічна стрижка</option>
                            <option>Догляд за кігтиками та вушками</option>
                            <option>Масаж лапок</option>
                        </select>
                    </div>

                    <div className="form-field">
                        <label className="form-label" htmlFor="serviceDate">Дата візиту</label>
                        <input className="form-input" type="date" id="serviceDate" name="serviceDate" min = {today} value={form.serviceDate} onChange={handleChange}/>
                    </div>


                    <div className="form-field">
                        <label className="form-label" htmlFor="serviceTime">Час візиту</label>
                        <input className="form-input" type="time" id="serviceTime" name="serviceTime" min="10:00" max="16:00" value={form.serviceTime} onChange={handleChange}/>
                        <span className="form-hint">Запис ведеться лише на рівні години (10:00, 11:00)</span>
                    </div>


                    <div className="form-field">
                        <label className="form-label" htmlFor="catMass">Вага, кг</label>
                        <input className="form-input" type="number" id="catMass" name="catMass" min="1" max="20" step="0.1" placeholder="Введіть масу кота..." value={form.catMass} onChange={handleChange}/>
                    </div>

                    <div className="form-field form-check">
                        <label className="form-label" htmlFor="agr_confirmation">Агресивна тварина</label>
                        <input className="form-checkbox" type="checkbox" id="agr_confirmation" name="agr_confirmation" checked={form.agr_confirmation} onChange={handleChange}/>
                    </div>

                    {error && <p className="error">{error}</p>}

                    <button type="submit" className="btn">Записати</button>

                </div>
                

            </form>
        </section>
    );
}

export default VisitForm;
