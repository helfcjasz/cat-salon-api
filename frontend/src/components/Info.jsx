function Info(){
    return(
        <div className="sections">
            <section className="section" id="services">
                <h2 className="section-title">Послуги</h2>
                <ul className="list">
                    <li>Купання та сушіння делікатними засобами</li>
                    <li>Вичісування та видалення ковтунів</li>
                    <li>Гігієнічна стрижка</li>
                    <li>Догляд за кігтиками, вушками та очима</li>
                    <li>Масаж лапок</li>
                </ul>
            </section>

            <section className="section" id="steps">
                <h2 className="section-title">Як проходить візит</h2>
                    <ol className="list">
                        <li>Знайомство кота з майстром</li>
                        <li>Огляд шерсті та шкіри</li>
                        <li>Купання або вичісування</li>
                        <li>Сушіння та фінальний догляд</li>
                    </ol>
            </section>

            <section className="section" id="faq">
                <h2 className="section-title">Часті запитання</h2>
                <details className="faq-item">
                    <summary className="faq-question">Скільки триває візит?</summary>
                    <p className="faq-answer">Від 40 хвилин до 2 годин залежно від довжини шерсті та обраної послуги.</p>
                </details>
                <details className="faq-item">
                    <summary className="faq-question">Чи можна приходити з кошеням?</summary>
                    <p className="faq-answer">Так, але купати кошенят можна <mark>з 3 місяців</mark>, після першої вакцинації.</p>
                </details>
                <details className="faq-item">
                    <summary className="faq-question">Як часто потрібно вичісувати мейнкуна?</summary>
                    <p className="faq-answer">Для довгошерстих котів — <strong>щонайменше раз на тиждень</strong>, а під час линьки частіше.</p>
                </details>
            </section>
        </div>
    )
}


export default Info;