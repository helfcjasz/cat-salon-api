import catPhoto1 from '../img/3.jpg';
import catPhoto2 from '../img/4.jpg';


function About() {
    return (
        <section className="section about" id="about">
            <h2 className="section-title">Про салон</h2>
            <div className="about-grid">
                <div className="about-text">
                    <p className="text">«Мейн-Мур» — це салон грумінгу для котів, де кожен гість стає <strong>головним пухнастиком дня</strong>. Ми працюємо спокійно, без поспіху й без гучних звуків, щоб візит був приємним і для кота, і для його господаря.</p>

                    <h3 className="subtitle">Чому саме мейнкуни?</h3>
                    <p className="text">Мейн-кун — одна з найбільших порід домашніх котів: з довгою шовковистою шерстю, пухнастим хвостом і китицями на вухах. Така шерсть дуже гарна, але вона <em>потребує регулярного догляду</em>, інакше в ній швидко з'являються ковтуни.</p>
                    <p className="text">Ми добре знаємо особливості цієї породи, тому для мейнкунів підбираємо окремі гребінці та делікатні засоби. Водночас до нас охоче приходять коти інших порід — усім знайдеться місце на м'якому килимку.</p>

                    <h3 className="subtitle">Як ми працюємо?</h3>
                    <p className="text">Перед процедурою кіт знайомиться з майстром і спокійно оглядає кімнату. Усі етапи проходять у <mark>комфортному для тварини темпі</mark>, з перервами на відпочинок і ласки.</p>
                    <p className="text">Після грумінгу кожен відвідувач отримує смаколик, а господар — пораду, як доглядати за шерстю вдома між візитами.</p>
                </div>

                <div className="about-media">
                    <div className="photo-frame">
                        <img className="photo" src={catPhoto1} alt="незадоволений кіт" />
                    </div>

                    <figure className="figure">
                        <div className="photo-frame">
                            <img className="photo" src={catPhoto2} alt="незадоволений кіт2"/>
                        </div>
                        <figcaption className="caption">Наші клієнти</figcaption>
                    </figure>
                </div>

            </div>
        </section>

    );


}


export default About;