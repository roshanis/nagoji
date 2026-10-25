# Horse of the Servant, graphic novel V15

## Chapter 24: Under De Lannoy's Standard

Source: `book1_horse_servant/book4_chapter24_under_de_lannoys_standard.md`, 8,326 words, adapted as 30 pages; every placed frame must reach 300 PPI or more at its printed size.

### Cast and look notes for this chapter

- **Nagoji, pages 1 to 13 (NOT yet in uniform):** Ananthan Pillai look. Kerala topknot, no turban, white mundu with shoulder cloth, bare arms, silver chain of office, no coat, no sash, no bandages, no knife. First grey at the temples. The old brand on the inner left wrist shows because his arms are bare. Constants in every panel: thick curled moustache, CLEAN-SHAVEN chin, small gold ear stud, long curly black hair bound in the topknot, no forehead mark. The chapter 22 palm cut has healed to a thin pale line across the left palm.
- **Nagoji, page 14 onward (uniform):** white European-cut coat, red waistcoat, plain undecorated brass buttons, knee breeches, buckled European riding boots (the cavalry officer's pattern; the infantry kit laid out at 5.2 has buckled shoes), silver chain of office worn over the coat, topknot, no hat, no turban, no sash, talwar at the hip. Same constants. No bandages, no knife.
- **For the author: CONTINUITY.md needs one amendment.** Its row for chapters 17 to 27 says "Ch24 onward in uniform", and `pipeline/script_pipeline.py` injects that whole row into every Nagoji prompt as authoritative. Until the row reads "Ch24 from the issue of the coats (script page 14) onward", pages 1 to 13 depend on the per-panel look lines below and are at risk of being drawn in the coat. The same row also carries the chapter 22 bandages and the chapter 17 to 20 knife, so every Nagoji panel here says "no bandages, no knife".
- **Distinguishing Nagoji among officers:** in every multi-officer panel he is nearest the camera or lit, and he is the only officer with a silver chain of office and no forehead mark. The Nair captains are older or heavier men with sandal-paste or ash marks on their foreheads.
- **De Lannoy:** tall, pale hair, bare-headed, pale freckled hands. A worn white Travancore coat throughout, patched at the elbows, frayed at the cuffs. He never wears Dutch blue in this chapter.
- **Troops before the coats (pages 1 to 13):** Nair musketeers in white mundu hitched at the knee, bare-chested or in short cotton jackets, with long muskets; Maravar horse in their own cloth with red shoulder cloths. No uniforms, no coats. From page 14 the drilling men wear the white coats.
- **The Goa officer (stains only, 6.5 and 11.1 to 11.3):** a pale European. Clean-shaven pale jaw, hair tied in a queue under a black tricorne, a deep-cuffed white coat edged with gilt lace, a column of ornate gilt buttons, a red waistcoat beneath, a smallsword at the hip. The frame always cuts off at his chin and his eyes are never shown. His coat is visibly a different cut from the Travancore coat, and his buttons are ornate where theirs are plain.
- **Portuguese in Goa:** gaol guards in dented steel morion helmets, loose off-white shirts, buff leather jerkins, dark breeches and buckled shoes, nothing red or blue. Portuguese soldiers in long white coats with red cuffs and red waistcoats, white-dominant, black tricornes; they must not read as British redcoats.
- **The standard (1.1, 1.4, 30.4):** the royal standard is red with a silver conch. Below it hangs De Lannoy's pennant, which is white with a dark blue diagonal line crossed by a dark blue curved line. Use this wording every time. The red and the conch follow the chapter 22 script; the novel gives the pennant no colours, so these are a placeholder the author may change, in all three panels at once.
- **Father Duarte:** in the present (pages 15 to 20) he is older and greyer, per CONTINUITY. In the stains (16.1, 19.2, 19.3) he is more than a decade younger, with his hair still dark and no grey. Never a white collar tab.
- **The Prince:** about fourteen in the present. In the stains (21.3, 26.5) he is about ten.
- **Cast overrides:** `scripts/CHAPTER-24-CAST-OVERRIDES.json`. Pass it with `--cast-overrides` so the stains and the Goa officer do not get Nagoji's chapter 24 sheet.

---

## PAGE 1

Five panels. The foreigner's tooth, the combined drill, the banner. Open on two men who have become a partnership, and end on the resentment it breeds. Nagoji is not yet in uniform, and no soldier wears a coat.

**1.1** Wide, full page width. A new star-fort bastion of laterite and packed earth jutting from the fort wall like an angled tooth, seen from below and to one side. Dry-season light, red dust hanging in the air. On its point, two small figures under a banner staff: the royal standard, red with a silver conch, at the top; below it a smaller pennant, white with a dark blue diagonal line crossed by a dark blue curved line.

> CAPTION: By the first dry season after Kollamkara's valley, the fort had a name for the new bastion.

> CAPTION: The foreigner's tooth. Half in jest, half in grudging respect.

**1.2** From the bastion, looking down on the drill ground. Maravar horse in their own cloth (white mundu hitched, short cotton jackets, red shoulder cloths) wheeling in pairs between marked posts along the base of the wall. Behind them a rank of Nair musketeers in white mundu hitched at the knee, bare-chested or in short cotton jackets, firing a controlled volley over the horses' backs at wooden targets in the scrub. No uniforms, no coats. A small field gun recoiling on well-braced wheels, white smoke rolling.

> CAPTION: A drill that would have made my younger self, and De Lannoy's old company captains, splutter.

**1.3** On the bastion. De Lannoy: tall, pale hair, bare-headed, a worn white Travancore coat patched at the elbows, shading his eyes with one hand. Nagoji beside him, arms folded, NOT yet in uniform: Kerala topknot, no turban, white mundu with shoulder cloth, silver chain of office, no coat, no sash, no bandages, no knife; first grey at the temples, clean-shaven chin, thick curled moustache, small gold ear stud.

> LANNOY: They are improving.

> NAGOJI: You sound almost pleased.

> LANNOY: Almost.

**1.4** Low angle up the staff. At the top, the royal standard, red with a silver conch. Beneath it, a smaller pennant, white with a dark blue diagonal line crossed by a dark blue curved line. Both snapping in the wind against a hard blue sky.

> CAPTION: A line for the wall. A curve for the horse. He had drawn it himself.

> LANNOY (off): If you insist on naming bastions after me, I insist on at least choosing a decent symbol.

**1.5** Full width, bottom. The two men from behind, looking out over the drill, the point of the tooth aimed outward at the scrub and the hills. Nagoji's black topknot and bare shoulders under the shoulder cloth, the silver chain glinting; De Lannoy taller beside him in his white coat.

> NAGOJI: Better a tooth than a sore. At least this one bites outward.

> CAPTION: Not everyone liked how sharp that bite was becoming.

---

## PAGE 2

Five panels. The court resents the foreigners. On the rampart, Lannoy names the danger and plants "kings fall" for the chapter's last page.

**2.1** The palace hall. Chiefs and officers seated along the walls, most with sandal-paste or ash marks on their foreheads. A heavy older Nair chief with ash stripes on his forehead leaning toward his neighbour, deliberately loud, eyes sliding to the far end of the hall where Nagoji and De Lannoy stand together. Nagoji not yet in uniform (topknot, white mundu and shoulder cloth, silver chain of office, no coat, no bandages, no knife); De Lannoy in his white coat.

> NAIR CHIEF: The Deccan rider and the Dutch captain.

> NAIR CHIEF: Two foreigners teaching us how to use our own land.

**2.2** Padmini Amma (in her fifties, thick black hair coiled at the nape and beginning to grey, simple gold, cotton sari, long walking stick) turning her head toward him, unhurried.

> PADMINI: Teaching us how to keep it.

> PADMINI: If you prefer to learn from men who have never seen a European musket up close, that is your choice. Do not complain when your sons bleed for it.

**2.3** Evening. The long rampart walk. Nagoji (not yet in uniform: topknot, white mundu and shoulder cloth, silver chain of office, no coat, no bandages, no knife) and De Lannoy side by side. Below them on the drill ground, a ragged line of Nair musketeers in white mundu, no uniforms, with gaps where men should be standing.

> CAPTION: Still, the resentment was there.

> LANNOY: We must not become a separate standard. If they see us as a force within a force, we will be cut out like a tumour when the monarchy changes.

**2.4** Lannoy shrugging, eyes on the palace roofs below. Nagoji watching him sidelong.

> NAGOJI: You think that will happen?

> LANNOY: In my land, kings fall. In yours, too.

**2.5** Full width. The palace roofline spread below the rampart in the dusk, tiled roofs stepping down toward the audience hall where the throne platform stands. The two men small on the rampart above it, Lannoy beginning to laugh.

> NAGOJI: We fight for the structure, then. Not the man.

> LANNOY: We fight so that whoever sits on that platform cannot easily undo what we have built. It is a selfish defence, in a way.

> NAGOJI: Selfish defence keeps people alive.

---

## PAGE 3

Five panels. The partnership at work: Ramayyan as balancer, then one recruit who learns from both men.

**3.1** A map table. Ramayyan (thin, sharp fine features, receding hair, plain white cloth, a palm-leaf bundle and stylus) standing between Nagoji and De Lannoy, who lean on the table from opposite sides over a plan of a wall. Nagoji not yet in uniform (topknot, white mundu and shoulder cloth, silver chain of office, no coat); De Lannoy in his white coat.

> RAMAYYAN: Stone where you must. Earth where you can.

> NAGOJI: You spend as much time keeping us from killing each other as keeping the king alive.

> RAMAYYAN: It is all the same work. Preventable deaths exhaust me.

**3.2** A hot afternoon, combined drill. A young Nair musketeer, barely more than a boy, in a white mundu hitched at the knee, bare-chested, no uniform, has fired too early: smoke at his muzzle, a spurt of dust far wide of the wooden target. De Lannoy striding toward him.

> LANNOY: Again.

**3.3** The youth fumbling at his powder horn, hands shaking. Behind him Nagoji trots past on Kayal, his bay mare with the ochre red-brown coat, mundu hitched for the saddle, turning to call down. Nagoji not yet in uniform: topknot, shoulder cloth, silver chain of office, no coat.

> NAGOJI: Breathe. The gun does not fear your heartbeat.

> NAGOJI: Make it go slower than the drum.

**3.4** Later, wide. The same recruit in a line of Nair musketeers in white mundu, no uniforms, firing in perfect time, muzzles angled high over a pair of Maravar riders cantering past below. De Lannoy (white coat) and Nagoji (topknot, white mundu, no coat) at the edge of the frame, both nodding.

> LANNOY: Good.

> NAGOJI: Now do it when someone is shouting in your ear.

**3.5** The boy grinning, sweat running into his eyes, musket grounded.

> RECRUIT: Yes, Kappittan. Yes, Pillai.

> CAPTION: He did not care which of us got which title.

---

## PAGE 4

Five panels. The world beyond the fort, and Revathi's warning. End on her one-word verdict so the king's demand can land on the turn.

**4.1** Evening on a lamplit verandah. Ibrahim Marakkar (short coat over a vest with bulging pockets, scar from the left ear to the jaw) with a cup of toddy. Padmini beside him, her stick across her knees. Nagoji listening, not yet in uniform (topknot, white mundu and shoulder cloth, silver chain of office, no coat, no bandages, no knife).

> IBRAHIM: The Dutch are no longer the only storm. There are new flags at the northern ports.

> PADMINI: We will need more than one tooth. And more than one kind of jaw.

**4.2** Velinadu, a courtyard in daylight. Revathi Bayi (deep indigo sari with gold, jasmine in her braid, flat-coin necklace, gold armlets, sandalwood line at the hairline, a tali at her throat, first grey threading her hair) seated at a low table beside an old steward, going through a bundle of palm-leaf accounts, a brass grain measure at her elbow. She does not look up. Nagoji standing before her, not yet in uniform (topknot, white mundu and shoulder cloth, silver chain of office, no coat).

> REVATHI: You and De Lannoy are useful.

> REVATHI: You are also convenient scapegoats.

**4.3** Revathi handing a palm leaf back to the steward without looking at it; her eyes are on Nagoji now. Nagoji, one eyebrow up.

> NAGOJI: Scapegoats?

> REVATHI: If the army fails, they will say the foreigner misled it. If it grows too strong, they will say the foreigner twisted it.

**4.4** Wide. Revathi has risen and the steward is going. Her gaze has drifted past Nagoji and out through the open courtyard gate to the south, where far off, small and grey above the palms, stands the angled point of the fort's new bastion.

> REVATHI: If a wall ever falls, I would rather it land on the Dutchman who designed it than on my people.

**4.5** Two-shot. Her hand rests flat on the stack of palm leaves. She is not smiling.

> NAGOJI: You make the future sound bleak.

> REVATHI: I make it sound like what it often is.

> REVATHI: Complicated.

*Page turn.*

---

## PAGE 5

Five panels. The king's demand. Give the coat its reveal.

**5.1** Wide. The war hall at night, lamplit, maps pinned to the walls. A dozen officers in their own clothes, no uniforms: Nair captains, older and heavier men with sandal-paste or ash marks on their foreheads; Maravar commanders with red shoulder cloths; a few men of the hired Madurai regiment in turbans. Nagoji among them, nearest the camera and lit: not yet in uniform (topknot, white mundu and shoulder cloth, no coat), the only officer with a silver chain of office and no forehead mark, small gold ear stud, first grey at the temples. De Lannoy apart, near the maps, in his white coat, his face carefully blank. At the head of the table, Marthanda Varma (V13 varma-v1 face, cream and gold, bare-headed, his hair in a side knot above his left ear, no turban, no crest, gold necklaces) holding up a coat like a trophy.

> CAPTION: The king's next demand made Revathi's complications feel almost simple.

> VARMA: This is what my army will wear.

**5.2** Insert, tight on the table as the uniform is laid out: a long white cotton coat of European cut with a column of plain, undecorated brass buttons catching the lamplight, a red waistcoat, knee breeches, stockings, buckled shoes.

> *No text. Let the buttons shine.*

**5.3** Varma, one hand flat on the coat.

> VARMA: The drill is European. The muskets are European. The forts are built to European designs.

> VARMA: It is time the men who use these things look as if they belong to the same army.

**5.4** An older Nair captain, heavy and grey, ash stripes on his forehead, shifting his weight, careful.

> NAIR CAPTAIN: Maharaja, our men have always worn...

> VARMA (off): What they pleased.

**5.5** Full width. Varma leaning over the table toward the room, the white coat under his hands.

> VARMA: When a Dutch officer looks through his glass at my lines, I want him to see something that makes his stomach turn.

> VARMA: Not a rabble. A machine.

---

## PAGE 6

Five panels. The logic is sound, and Nagoji sees Goa.

**6.1** Varma turning toward De Lannoy at the maps.

> VARMA: You have seen European armies. Tell them.

**6.2** De Lannoy stepping forward to the table, the room's eyes on him.

> LANNOY: In Europe, when regiments dress alike, they move alike.

> LANNOY: When an enemy sees a line of men dressed the same, he sees not individuals but a wall. Walls are harder to break than crowds.

**6.3** Varma.

> VARMA: And when those walls wear coats like his own army's, the enemy hesitates. He wonders if his maps are wrong.

> VARMA: Hesitation kills.

**6.4** Nagoji among the officers, nearest the camera, looking at the coat on the table: not yet in uniform (topknot, white mundu and shoulder cloth, silver chain of office, no coat, no bandages, no knife), no forehead mark. At the edges of the frame the other officers, older men with forehead marks, nod. He does not.

> CAPTION: The logic was sound.

> CAPTION: But I did not see logic.

**6.5** Full width, bottom. Bleeding in from the panel edge like a stain, not a clean flashback frame: a stone corridor in Goa, slick with monsoon damp. Far down the corridor, two Portuguese soldiers in long white coats with red cuffs and red waistcoats, black tricornes, walking away (white-dominant, not redcoats). Nearer, the Goa officer: a pale European, clean-shaven pale jaw, hair tied in a queue under a black tricorne, a deep-cuffed white coat edged with gilt lace, ornate gilt buttons, a red waistcoat, a smallsword at his hip; the frame cuts off at his chin and his eyes are never shown; he is adjusting one cuff. Behind him, two Portuguese gaol guards (dented steel morion helmets, loose off-white shirts, buff leather jerkins, dark breeches; nothing red or blue) dragging two chained prisoners: Keshavrao (about nineteen, beardless apart from a faint youthful moustache, narrow shoulders, black hair hacked short, faded grey-brown torn tunic) and, seen from behind, Nagoji in his captivity rags (torn ochre sleeveless tunic, cream dhoti, bandaged hands, ankle irons, barefoot, long curly hair loose). The guards' buckled shoes on wet stone.

> CAPTION: I saw Goa.

*Page turn.*

---

## PAGE 7

Five panels. The king notices, answers every objection, and dismisses the room.

**7.1** Back in the hall, the stain fading at the panel edge. Tight on Nagoji's throat and jaw: clean-shaven chin, thick moustache, the silver chain at his collarbone, the edge of his shoulder cloth. No coat.

> CAPTION: The coat was not Portuguese. The cut was different, the buttons plain rather than ornate.

> CAPTION: But the colour, the shape, the entire idea of wrapping myself in European cloth...

**7.2** Varma across the table, his eyes on Nagoji.

> VARMA: You have concerns, Pillai.

> CAPTION: It was not a question.

**7.3** Two-shot across the table, the white coat lying between them. Nagoji answering, level: not yet in uniform (topknot, white mundu and shoulder cloth, silver chain of office, no coat). Varma listening.

> NAGOJI: I have served you in my own clothes. They have not prevented me from drilling your horse.

> VARMA: No. But your horse are a small part of this army. When the full force marches, I want one face. Not many.

**7.4** Over Nagoji's shoulder onto Varma, the coat's plain brass buttons in the foreground.

> NAGOJI: The men will resist. They will see this as...

> VARMA: Foreign. Yes. As they saw muskets once. As they saw star forts.

> VARMA: They learned. So will you.

**7.5** Wide. Varma addressing the room. The officers, men with forehead marks, already turning for the door. Nagoji not moving, the only man with a silver chain of office and no forehead mark.

> VARMA: Coats will be issued within the month. Officers will set the example.

> VARMA: Dismissed.

---

## PAGE 8

Five panels. Alone with the king. He sees exactly what Nagoji sees.

**8.1** The emptied hall. Only the two of them and the lamps. Varma not looking up from the coat. Nagoji not yet in uniform (topknot, white mundu and shoulder cloth, silver chain of office, no coat, no bandages, no knife).

> VARMA: You are thinking of Goa.

> NAGOJI: I am thinking of many things.

**8.2** Varma lifting the coat, holding it at arm's length.

> VARMA: You are thinking that this coat looks like the coat of the men who broke your fingers and chained you in a ship's hold.

> VARMA: It is not the same coat. The men who wear it will not be the same men.

**8.3** Nagoji's hand, ridged fingernails, the old brand at the inner left wrist, stopped a finger's width above one plain brass button of the coat. His face above it, out of focus.

> NAGOJI: Knowing and feeling are different animals.

**8.4** Varma setting the coat down on the table between them.

> VARMA: Yes. They are. But I do not have time to wait for your feelings to catch up with your knowledge.

> VARMA: Other Europeans will come. When they do, I want them to see an army that they recognise and fear.

**8.5** Full width. Varma at the window, his back to the room, night outside. Nagoji alone at the table with the white coat.

> VARMA: Talk to De Lannoy. He wears the coat already.

> VARMA: Ask him how it sits on a man who once wore a different one.

---

## PAGE 9

Four panels. The bastion at sunset. Lannoy tells his own story first. The light moves across pages 9 to 13: sunset, then dusk, then last light, then the first lamps.

**9.1** Wide. The foreigner's tooth at sunset, the training ground below painted copper and dust, the evening drill underway (men in white mundu, no coats yet). De Lannoy at the parapet with a cup of toddy, not turning. Nagoji climbing the last steps, not yet in uniform (topknot, white mundu and shoulder cloth, silver chain of office, no coat, no bandages, no knife).

> LANNOY: You stayed behind. I assume you did not simply want to admire the buttons.

> NAGOJI: The king told me to speak with you. About wearing the coat.

> LANNOY: Ah.

**9.2** Low angle along the parapet. De Lannoy turning the cup slowly in his pale hands, eyes on the drill below, not on Nagoji. The sun low behind the far hills.

> LANNOY: When the fort burned at Colachel, I expected to die.

> LANNOY: What I did not expect was to be offered a choice.

**9.3** Lannoy, a soft laugh into his cup. Nagoji at his shoulder, watching him.

> LANNOY: Serve Travancore, or rot in a cell until the company forgot my name.

> LANNOY: They would not have lifted a finger. I knew too much about their failures.

> LANNOY: Dead men cannot testify.

**9.4** Full width. Lannoy turned to face Nagoji, the sunset behind him.

> LANNOY: The first time I put on Travancore colours, I felt as if I had swallowed broken glass.

> LANNOY: My mother would light candles for a son who had become, in their eyes, a traitor.

---

## PAGE 10

Five panels. Cloth, choice, thread. Dusk. End on the officer.

**10.1** Close on De Lannoy looking down at his own coat, thumbing the patch at the elbow: the same white cotton the king displayed, worn soft.

> NAGOJI (off): And now?

> LANNOY: Now it is cloth. It keeps the sun off my shoulders and the rain off my back.

**10.2** Low angle from the drill ground up at the parapet: De Lannoy in silhouette against the dusk sky, Nagoji a darker shape beside him, topknot against the light.

> LANNOY: The man inside has not changed. He has simply learned to wear a different skin.

**10.3** Close on Nagoji's hand gripping the parapet stone: ridged fingernails, the old brand at the inner left wrist, bare forearm, the edge of his shoulder cloth. No coat sleeve.

> NAGOJI: You chose this. You accepted the king's offer.

> NAGOJI: I did not choose to look like a Portuguese guard.

**10.4** Over De Lannoy's shoulder, looking down: the men below falling into formation in white mundu, no coats yet, their lines drawn like threads being pulled into a weave.

> LANNOY: No. But you chose to stay. To drill these men. To build these walls with me.

> LANNOY: Each of those choices was a thread. The coat is simply the weaving.

**10.5** Full width. Nagoji leaning on the parapet, looking past the drill ground to the distant line of the sea, the colour going out of the sky. Not yet in uniform (topknot, white mundu and shoulder cloth, silver chain of office, no coat).

> NAGOJI: In Goa, there was an officer.

> NAGOJI: He was very particular about his cuffs.

*Page turn.*

---

## PAGE 11

Five panels. The memory, shot as stain, then back to the bastion at dusk. Nothing on the floor is ever shown.

**11.1** Full width. The stain takes the whole panel: a Goa corridor in grey dawn light, outside a cell door. The Goa officer: a pale European, clean-shaven pale jaw, hair tied in a queue under a black tricorne, a deep-cuffed white coat edged with gilt lace, a column of ornate gilt buttons, a red waistcoat beneath, a smallsword at his hip. The frame cuts off at his chin; his eyes are never shown. He draws one cuff straight with two fingers. Behind him, two Portuguese gaol guards waiting (dented steel morion helmets, loose off-white shirts, buff leather jerkins, dark breeches; nothing red or blue).

> NAGOJI (off): He would come each morning, and check his cuffs before he gave orders.

**11.2** Tight on the officer's buckled shoe, an ornate silver buckle, lifting carefully over wet flagstones. The deep white cuff of his coat at the top of the frame. Whatever is on the floor stays out of frame.

> NAGOJI (off): The coat was always clean. Even when there was blood on the floor.

> NAGOJI (off): He would step around it, so as not to stain his shoes.

**11.3** From inside the cell, low, looking toward the door: the officer's white back leaving, the heavy door swinging shut behind him. At the top edge of the frame, a pair of empty iron manacles on a short chain hangs slack from a ring in the wall.

> NAGOJI (off): Then he would leave, and the guards would do what he had ordered.

> NAGOJI (off): And the coat would walk out as spotless as it had walked in.

**11.4** Back on the bastion at dusk. De Lannoy, quiet, turned toward Nagoji; Nagoji still looking at the sea (topknot, white mundu and shoulder cloth, silver chain of office, no coat).

> LANNOY: And when you see this coat...

> NAGOJI: I see his cuffs. I see his shoes. I see the door closing behind him while I hung from the chains and wondered how many more mornings I could survive.

**11.5** Wide. Below, a drummer beating the evening call, men in white mundu forming up for the last drill of the day, no coats yet. The two men small at the parapet.

> LANNOY: I cannot make that memory disappear. No one can.

> LANNOY: But I can tell you what I have learned about clothes and men.

---

## PAGE 12

Five panels. Last light. Lannoy's argument, and the challenge that lands. End on Nagoji's pushback.

**12.1** Over their shoulders: De Lannoy moving to stand beside Nagoji, both looking down at the training ground, the last light long across it.

> LANNOY: In Zeeland, where I was born, there is a saying: the shirt does not make the sailor, but it tells you which ship he serves.

> LANNOY: I simply chose a different ship.

**12.2** Close on Nagoji turning his head toward him (topknot, silver chain of office, no coat).

> NAGOJI: And if the ship is wrong?

> LANNOY: Then you are wrong with it. But you are wrong *together*.

> LANNOY: That is what the coat means. When you stand in a line with these men, you are telling the world: we fight as one.

**12.3** Tight on De Lannoy's pale hand setting his empty cup on the parapet stone; his face above it, turned to Nagoji.

> LANNOY: The Portuguese who tortured you were not evil because of their coats.

> LANNOY: They were evil because of what they chose to do while wearing them.

> LANNOY: You have the same choice.

**12.4** De Lannoy squared to face him, the last light on one side of his face, the drill ground dim behind.

> LANNOY: You can wear this cloth and be the man who trains cavalry to protect Padmini's fields.

> LANNOY: Or you can refuse, and be the man who could not see past his scars to what his king was building.

**12.5** Full width. Nagoji's face in the last light, jaw set: not yet in uniform (topknot, silver chain of office, shoulder cloth, no coat).

> CAPTION: The words struck harder than I wanted to admit.

> NAGOJI: You make it sound simple.

---

## PAGE 13

Three panels. The glass, the recruit below, and the decision. Give the decision half the page. First lamps along the wall.

**13.1** De Lannoy, rueful, less composed than we have seen him, looking down at his own frayed cuff. Nagoji beside him, not yet in uniform (topknot, white mundu and shoulder cloth, silver chain of office, no coat).

> LANNOY: It is not simple.

> LANNOY: Some mornings I look at the coat on its peg and feel that glass in my throat again.

**13.2** Wide, looking down past the two men at the parapet: on the drill ground below, in the dim light, a young recruit (white mundu, no coat) has fumbled his musket drill; an officer shouts; the boy corrects himself. The first lamps being lit along the wall.

> LANNOY: Then I put it on. And I go to the wall. And I do the work.

> LANNOY: Eventually, the glass becomes smaller.

**13.3** Half the page. Nagoji's face in the last of the light, lamplight starting on one cheek: not yet in uniform (topknot, silver chain of office, shoulder cloth, no coat, no bandages, no knife). At the panel edge, one faint stain: Keshavrao's thin young face, black hair hacked short.

> CAPTION: The coat was cloth. The man inside would still be me.

> NAGOJI: I will wear it.

*Page turn.*

---

## PAGE 14

Five panels. Lannoy's dry blessing, then the coat goes on. From here on Nagoji is in uniform (see the cast notes).

**14.1** De Lannoy nodding once. No smile, no hand on the shoulder. One soldier acknowledging another. Lamplight on the parapet.

> LANNOY: The first few days will be difficult. You will want to tear it off and burn it.

> LANNOY: I recommend against burning it. The quartermaster is very particular about inventory.

> NAGOJI: I will try to restrain myself.

**14.2** Nagoji's quarters, small and bare. A small bronze mirror on the wall. Nagoji in the uniform for the first time: white European-cut coat, red waistcoat, plain brass buttons, knee breeches, buckled European riding boots, silver chain of office worn over the coat, topknot, no hat, no turban, no sash; clean-shaven chin, thick curled moustache, gold ear stud, grey at the temples. No bandages, no knife. His reflection in the bronze is dimmer and warmer than the man.

> CAPTION: The coats arrived a week later.

> CAPTION: For a long moment I was looking at a stranger.

**14.3** Tight on his hands drawing one white cuff straight with two fingers: a brown hand, ridged fingernails, plain brass buttons on the cuff. The gesture mirrors the Goa officer's in 11.1 exactly; the plain buttons and the brown hand are what differ.

> CAPTION: The way that officer in Goa had done.

**14.4** The drill ground. Nagoji walking out in uniform, silver chain over the coat, talwar at his hip. His troop of Maravar riders, now in the same white coats, turning to stare; a few mutter behind their hands; one young horseman's laugh dying on his face as he meets Nagoji's eyes.

> NAGOJI: The same drills. Different cloth.

> NAGOJI: Mount up.

**14.5** Full width. The troop swinging into their saddles as one, Nagoji already mounted at their head on Kayal, his white coat and silver chain bright against the red dust.

> CAPTION: And we began.

---

## PAGE 15

Four panels. The Portuguese embassy. Withhold the priest's face until the last panel, and give that panel half the page.

**15.1** Wide. The parade ground, a squad of musketeers in the new white coats running drill. Through the gate rides a small embassy: three men in dark cloth, a secretary with a record book under his arm, and a thin figure in black on a mule under a broad travel hat. Nagoji in the foreground in uniform (white coat stiff across his shoulders, red waistcoat, plain brass buttons, silver chain of office over the coat, topknot, no hat).

> CAPTION: The Portuguese came two weeks after the coats.

> CAPTION: Not with ships or guns. With letters and gifts, and a priest.

**15.2** Ramayyan appearing at Nagoji's elbow, already half turned toward the palace.

> RAMAYYAN: The Viceroy sends his compliments. And his curiosity. Pepper, as always.

> NAGOJI: The Dutch came for pepper too. We know how that ended.

> RAMAYYAN: The king wants them to see our officers.

**15.3** Nagoji turning to follow, and stopping mid-turn. His face arrested.

> *No text.*

**15.4** Half the page. His point of view across the yard to the stables. The priest dismounting: older, grey hair under the hat, the scholar's stoop deeper, ink on his fingers, a plain black cassock with a small cross and no collar tab. His right hand has slipped inside his sleeve and is worrying at the cloth. He is talking to his secretary and has not seen Nagoji.

> CAPTION: Father Duarte.

*Page turn.*

---

## PAGE 16

Five panels. More than a decade, crossed in a few paces.

**16.1** Across the top, bleeding like a stain: a vaulted stone interrogation chamber lit red by a brazier, an empty stool in shadow. Duarte more than a decade younger, hair still dark with no grey, thin, a plain black cassock with a small cross and no collar tab, inclining his head in a small, weary nod.

> CAPTION: More than a decade since he had asked me whether I believed in God or only in powder.

> CAPTION: Since he had hesitated.

**16.2** Tight on Nagoji's buckled European riding boots crossing packed red earth, the hem of the white coat swinging above them.

> CAPTION: The kind that had clicked on the stone floors of Goa.

**16.3** Duarte turning. Three narrow vertical slices of his face across the panel: polite greeting, then confusion, then recognition. Production: generate each slice as its own frame and composite them into the strip, so the face stays the same man.

> CAPTION: And then something I had not expected.

**16.4** Duarte, full face, afraid. His hands stay low; the right one twitches inside its sleeve.

> DUARTE: Senhor... I... that is...

> NAGOJI (off): Father Duarte. You have come a long way from Goa.

**16.5** Full width. Over Duarte's shoulder: his eyes moving over Nagoji, the white coat and silver chain, the talwar at the hip, the drilling men behind him who would come if he raised a hand.

> CAPTION: He was calculating, as I had calculated once, the distance between himself and safety.

---

## PAGE 17

Five panels. The survivor and the powder.

**17.1** Duarte, his voice catching. Behind him the secretary has stopped short, the record book clutched to his chest.

> DUARTE: You survived. The ship... we heard it was lost in a storm.

**17.2** Over Duarte's grey head and black shoulder onto Nagoji in uniform, level, the silver chain over the white coat.

> NAGOJI: Most of it was.

> NAGOJI: I did not.

**17.3** Duarte's hand rising toward the cross at his throat, then stopping short, as if the gesture would be inadequate.

> DUARTE: I have thought of you. Over the years. I have wondered...

> NAGOJI: Whether I would come for you?

**17.4** Low angle on Duarte, steadier, his hand gone back inside his sleeve and working at the cloth.

> DUARTE: Whether you found what you were fighting for.

> DUARTE: That night, in the chamber, you said God favours whoever has the better powder.

**17.5** Full width. Duarte's gaze across the parade ground: the white-coated lines, the star-fort walls, a field gun on its carriage.

> DUARTE: It seems you found the better powder.

> NAGOJI: I found something. Whether it is what I was fighting for, I am still deciding.

---

## PAGE 18

Five panels. The power is all on one side now. Let the silence stretch. End on the question, with no answer drawn.

**18.1** Wide. The two men small in the middle of the fort's business: horses led to water, an officer shouting commands, the secretary hovering at a distance, unsure whether to intervene.

> *No text.*

**18.2** Nagoji close to him, quiet.

> NAGOJI: I could have you arrested.

> NAGOJI: Some of these men lost brothers in your dungeons. Some of them lost more.

**18.3** Duarte, jaw tight. He does not look away.

> DUARTE: You could. It would not be unjust.

> NAGOJI: No. It would not.

**18.4** Narrow strip. Both faces, neither speaking.

> *No text. Hold it.*

**18.5** Tight on Nagoji alone, Duarte out of frame.

> NAGOJI: But I am not going to.

> NAGOJI: Do you know why?

*Page turn.*

---

## PAGE 19

Five panels. The payoff of chapters 1 and 2: the two hesitations, returned to the man who made them.

**19.1** Duarte's small shake of the head in the foreground, the back of his grey head and black shoulder; Nagoji beyond him, in uniform, answering.

> NAGOJI: Because you hesitated.

**19.2** Stain. A red-lit stone chamber. João's thick ruddy wrist in a rolled cream shirt sleeve under a brown leather jerkin, reaching toward a glowing brazier; Duarte's thin ink-stained hand, more than a decade younger, shooting out of a plain black cassock sleeve and gripping it. Only one cassock sleeve in the frame.

> NAGOJI (off): In the chamber, when João reached for the brazier, you stopped him.

**19.3** Stain. A Goa courtyard of whitewashed walls under glaring sun. Duarte more than a decade younger, hair still dark, in a broad round travel hat and a plain black cassock, making a slow, deliberate sign of the cross toward a chain of prisoners in grey, brown and ochre captivity rags. Portuguese musketeers in broad hats and buff leather coats along the wall, nothing red or blue.

> NAGOJI (off): At the gate, you made the sign of the cross. Not the quick one, the one that wards off evil.

> NAGOJI (off): The slow one. The one that asks for something.

**19.4** Duarte's eyes glistening. He blinks it away.

> *No text.*

**19.5** Duarte.

> DUARTE: I asked for your forgiveness.

> DUARTE: I have asked for it every day since.

---

## PAGE 20

Five panels. Not forgiveness. Something harder. He says it to Duarte's face, then walks away.

**20.1** Nagoji in uniform. Behind him, a faint stain: a thin young hand slipping from a rope in black storm water.

> NAGOJI: I cannot give you that. What was done to me is not mine alone to forgive.

> NAGOJI: Keshavrao drowned in that storm. Others died in your cells. Their forgiveness is not mine to grant.

**20.2** Nagoji stepping closer, the silver chain and plain brass buttons of the coat catching the light.

> NAGOJI: I wear this coat now. I drill these men.

> NAGOJI: The man you tortured is gone.

> NAGOJI: The man who stands here now has made his choices. Some of them haunt me. Some of them I am proud of. Most are somewhere in between.

**20.3** Duarte nodding slowly.

> DUARTE: Then we are alike in that. More than I would have thought.

> NAGOJI: Perhaps.

**20.4** Two-shot, face to face, an arm's length apart. Nagoji holds Duarte's eyes.

> NAGOJI: When you return to Goa, tell them what you saw here.

> NAGOJI: Tell them that the man they branded as property now commands the cavalry that guards this coast.

**20.5** Full width. Nagoji walking away across the parade ground in his white coat, his back to Duarte, toward the drilling lines. Small behind him, the secretary hurrying to Duarte's side.

> CAPTION: The glass in my throat, the one Lannoy had spoken of, was still there.

> CAPTION (separate, weighted): But it was smaller.

---

## PAGE 21

Five panels. The heir arrives. He is no longer ten.

**21.1** Wide. The drill ground in morning light. At its edge, the Prince, about fourteen: tall enough to look Nagoji in the chest, narrow in the shoulders, beardless, his uncle's sharp cheekbones and his mother's watchful eyes, in a plain training tunic with no silks or jewels. Two Nair guards a pace behind him, hands near their hilts. Nagoji facing him in uniform (white coat, red waistcoat, plain brass buttons, silver chain of office over the coat, topknot; no bandages, no knife).

> CAPTION: Three months after the coats.

> PRINCE: My uncle says I am to learn from you.

> NAGOJI: Learn what?

**21.2** Tight on the Prince. No self-pity. A flat statement of fact.

> PRINCE: How to stay alive when men want me dead.

**21.3** Inset, bleeding like a stain, in daylight: the great temple, its carved gopuram behind. The heir at ten, small, in white, frozen, eyes wide. A curved knife flashing down in a hand whose owner is out of frame. Between blade and boy, a man's shoulder in white silk turning in to take it. No blood. No face but the boy's. No priest.

> CAPTION: The King's blood on white silk.

**21.4** Two-shot, the Prince squared up to Nagoji.

> NAGOJI: Your uncle could have sent you to De Lannoy.

> PRINCE: De Lannoy teaches formations. My uncle says you teach survival.

**21.5** Nagoji looking past the Prince at the guards.

> NAGOJI: They stay at the gate. On the training ground, you are not a prince. You are a student.

> NAGOJI: If I strike you, they do not interfere. If you fall, they do not help you rise.

---

## PAGE 22

Five panels. He sends his own guards away, and the beating begins.

**22.1** The older guard, grey at his temples, stepping forward.

> OLD GUARD: Highness, the Maharaja's orders were...

> PRINCE: To learn from this man. I cannot learn if I am wrapped in silk. Go.

**22.2** The guards walking away toward the gate. The Prince turning back to Nagoji, the set of his jaw exactly his uncle's.

> PRINCE: What first?

**22.3** Nagoji, in uniform, tossing a wooden practice sword at the Prince's chest. The Prince catches it, barely.

> NAGOJI: First, you learn how much you do not know.

**22.4** Wide, a strip of three beats in one panel: the Prince's legs swept from under him; the Prince disarmed, his wooden sword spinning away; the Prince at dusk bowing to Nagoji, a fresh bruise on his forearm over a fading one. Production: generate each beat as its own frame and composite them into the strip, so the boy stays the same boy.

> CAPTION: He did not once ask to rest.

**22.5** Full width. The Prince taking a fall, rolling, and coming up with his sword ready. At Nagoji's shoulder, Ramayyan has appeared without a sound.

> RAMAYYAN: You are trying to kill the heir.

> NAGOJI: I am trying to make him harder to kill. There is a difference.

> RAMAYYAN: The Senior Rani has concerns.

---

## PAGE 23

Five panels. The Senior Rani comes to see for herself.

**23.1** The Prince mid-drill, his eyes flicking sideways and holding a heartbeat too long. Nagoji (in uniform) follows the look: in the shade of the armoury wall stands the Senior Rani of Attingal, in white without ornament, her hair pulled back severely, her face unreadable.

> NAGOJI: Continue. A king who is distracted by his mother will be distracted by everything.

**23.2** An hour later, the sun higher, dust hanging. Nagoji walking to her. Behind him, the Prince drinking deep from a water skin, his tunic dark with sweat.

> NAGOJI: Highness. You could have summoned me to the palace.

> SENIOR RANI: I wished to see. There is a difference between reports and observation.

**23.3** Her eyes on her son.

> SENIOR RANI: He has changed. The way he stands. Even the servants have noticed. And the cost?

> NAGOJI: Bruises. A few cuts that will scar. Nothing that will not heal.

**23.4** She turns to face him fully. Her voice drops.

> SENIOR RANI: When he was born, my brother held him and wept.

> SENIOR RANI: I have spent fourteen years keeping him alive. Tasters, guards, astrologers.

**23.5** Full width. Her face, hard.

> SENIOR RANI: Now I send him to you because all my counting has made him soft.

> SENIOR RANI: At the temple, he stood like a deer in torchlight.

> NAGOJI: He will not freeze again. I am burning that out of him.

---

## PAGE 24

Five panels. The coin, the threat, and the son's verdict.

**24.1** The Senior Rani, the faintest ghost of a smile.

> SENIOR RANI: I know. That is why I have not stopped you.

> SENIOR RANI: A mother's fear can become a son's chains.

**24.2** She presses something into his hand. Inset, tight: a small gold coin, old, worn smooth by generations of fingers, in Nagoji's open left hand: ridged fingernails, a thin pale healed scar across the palm, the white cuff and a plain brass button of his coat at the wrist.

> SENIOR RANI: This was my grandmother's. It passes from woman to woman in this house.

> NAGOJI: Then why give it to me?

**24.3** She takes the coin back.

> SENIOR RANI: I am not giving it to you. I am showing it to you.

> SENIOR RANI: So that you understand what you are training. Not a soldier. Not a prince. A line.

**24.4** Close on her face, perfectly calm.

> SENIOR RANI: If you break him, I will have you killed. Slowly. With full knowledge of what is happening to you.

> NAGOJI: I understand, Highness.

> SENIOR RANI: He says you tell him unpleasant truths. Continue.

**24.5** Full width. She walks away, back straight, steps measured. The Prince has come to Nagoji's elbow; both watch her go.

> PRINCE: She likes you.

> NAGOJI: She threatened to have me killed slowly.

> PRINCE: Yes. That is how you know. The ones she does not like, she simply has killed. Without warning.

---

## PAGE 25

Five panels. The horse lesson at dawn. The boy finally names the temple.

**25.1** Wide. Before dawn, the training ground empty and misted. Two small riders walking their horses in slow circles: Nagoji in uniform on Kayal, the Prince on a smaller grey.

> CAPTION: The second month.

> NAGOJI: In the Deccan, a man's horse is his second self.

> PRINCE: Our kings ride elephants.

> NAGOJI: Elephants are for show. A horse can take you where elephants cannot. Away from danger, when danger is the only certainty.

**25.2** Trotting side by side, the sun clearing the tree line, the world gone gold and green. The Prince looking straight ahead, not at Nagoji.

> PRINCE: Pillai. At the temple, when the chaver came, I froze.

> PRINCE: I saw the blade and I could not move. If my uncle had not...

**25.3** Both reined in, the horses facing each other.

> NAGOJI: He did. That is what matters.

> NAGOJI: You were ten years old. A boy can be forgiven.

> PRINCE: I am not ten now.

**25.4** Close on Nagoji, level, the low sun behind him.

> NAGOJI: If it happens again, your body will know what to do before your mind has time to be afraid.

> PRINCE (off): And if instinct is not enough?

> NAGOJI: Then you die. But you die moving, not standing still.

**25.5** Full width. The Prince looking at him for a long moment, the two horses standing in the gold light.

> PRINCE: You do not speak to me like the others do.

> PRINCE: The others speak around the truth. You speak through it.

---

## PAGE 26

Five panels. The third month. The heir in the line, and the boy who is gone.

**26.1** Wide. The drill ground. In the foreground, a Nair captain (older, heavier, ash stripes on his forehead) muttering to Nagoji (in uniform, silver chain over the coat, no forehead mark). Behind them, the Prince in the same white coat as the others, visibly the youngest and slightest man on the ground, beardless and narrow-shouldered, hauling a collapsed recruit into the shade and holding his own water skin to the man's lips.

> NAIR CAPTAIN: The heir cannot be treated like a common soldier.

> NAGOJI: That is the point.

**26.2** Evening on the bastion. The Prince, in his white coat, beside Nagoji at the parapet.

> PRINCE: The men look at me differently now.

> NAGOJI: They look at you as one of them. Is that not what you wanted?

> PRINCE: I do not know what I wanted.

**26.3** Close on the Prince, looking out over the training ground, not at Nagoji.

> PRINCE: I only knew I did not want to be the boy at the temple again. The one who stood there while others bled for him.

> NAGOJI (off): You will never be that boy again. You have made certain of it.

**26.4** Two-shot. The Prince rolling his shoulders the way he has been taught, then a small, wry smile.

> PRINCE: Thank you, Pillai. For not treating me like glass.

> NAGOJI: Glass breaks. You are iron that has not yet been forged. The fire is uncomfortable. But it is necessary.

> PRINCE: Then I will try to enjoy the burning.

**26.5** Full width. The Prince walking down from the bastion, past guards who no longer hover so close, past men who nod to him as a fellow soldier instead of bowing. Nagoji watching from above. At the panel edge, a faint stain: a ten-year-old boy in white standing in the courtyard of a Kerala house, wide-eyed.

> CAPTION: That boy was gone.

> CAPTION: In his place walked someone who might, one day, be worthy of the throne his uncle was building for him.

---

## PAGE 27

Five panels. The new master of the guns. End on Nagoji's challenge.

**27.1** The artillery yard. Thoma Ittyerah (broad, a white tunic, betel-stained teeth) crossing himself, one palm about to rest on the barrel of a bronze field gun. His mixed crew of Syrian Christians and Nairs waiting. Nagoji watching, in uniform.

> CAPTION: The artillery came under new command that season. Thoma Ittyerah.

> CAPTION: His people had been Christians on this coast long before any Portuguese ship troubled these waters.

**27.2** Thoma, a big hand flat on the gun.

> THOMA: My grandfather cast cannon for the Zamorin. My father cast them for Kochi. I cast them for Travancore.

> THOMA: The metal does not care which king pays for the mould.

**27.3** Thoma squinting along the barrel, adjusting the elevation.

> NAGOJI: You do not pray to the same gods as your men.

> THOMA: No. But we bleed the same colour. That is enough for a gun crew.

**27.4** Wide. The gun fires. Downrange, a wooden target bursts into splinters. The crew in fixed places around the gun, loader, rammer, the man with the slow match, each moving in exact ritual order.

> CAPTION: Their faith was not in any god, but in the mathematics of fire.

**27.5** In the drifting smoke, Thoma grinning through it, teeth stained dark red-brown with betel. Nagoji beside him in his white coat.

> THOMA: The Dutch and the Portuguese think history began when their ships arrived.

> THOMA: This coast has buried empires before them. It will bury more.

> NAGOJI: And yet we wear their coats now. And fire their cannons.

*Page turn.*

---

## PAGE 28

Five panels. Thoma's answer, the Jews of Kochi, and the long view.

**28.1** Close on Thoma as the smoke thins, unbothered, wiping his hands.

> THOMA: We wear what is useful. We fire what works.

> THOMA: That is not surrender. That is wisdom.

**28.2** Wide. A river dock, a small boat pulled in beside stacked barrels of saltpetre. Avraham ben Ephraim just stepped off: dark coat despite the heat, a cap, a beard that falls to his chest. Thoma's hand on Avraham's shoulder, presenting him. Avraham giving Nagoji's white coat a slow once-over; Nagoji answering with a half bow.

> THOMA: Avraham ben Ephraim. His family has traded with mine for four generations.

> AVRAHAM: The man who teaches horses to dance with muskets.

> NAGOJI: The man who tries.

**28.3** Thoma laughing, a hand on a barrel. Avraham unsmiling but not displeased.

> THOMA: The Jews of Kochi have a saying.

> THOMA: The Portuguese came and went, the Dutch came and are going, the English are coming. We remain.

**28.4** Another evening. Lamplight. Avraham and Thoma over cups of arrack, account books and manifests spread between them. Nagoji with them, his coat unbuttoned.

> AVRAHAM: I doubt all kings. But this king pays his debts. That is worth something.

> AVRAHAM: We have outlasted Pharaohs and Caesars and Inquisitors. We will outlast kings of pepper, too.

**28.5** Full width. Avraham's small boat going out into the dusk. Lamps being lit along the fort walls. Nagoji and Thoma small on the wall, watching it go.

> NAGOJI: Strange allies, these.

> THOMA: All allies are strange. Until you need them.

---

## PAGE 29

Five panels. The armoury. A blade offered hilt first. End on the title question.

**29.1** Evening in the fort's small armoury, the last daylight slanting through the open door, a lamp already lit on the racks of spears and a new shipment of blades. De Lannoy lifting a talwar, feeling its weight. Nagoji beside him in uniform.

> LANNOY: Your swords are better for cutting from horseback. Our straight blades are better for thrusts on foot.

> NAGOJI: We make do with what the land asks. If the ground is cluttered, curve your steel.

**29.2** Tight: De Lannoy has flipped the sword and offers it hilt first. Nagoji's brown hand, ridged fingernails, plain brass buttons at the white cuff, closing on the hilt; De Lannoy's pale freckled hand, from a frayed and much-mended cuff, still on the flat of the blade.

> LANNOY: If we are to be blamed together, we may as well be armed together.

**29.3** De Lannoy leaning against a rack of spears, staring at some point between them.

> NAGOJI: You have accepted that you will never go back.

> LANNOY: Back where? To ships that would call me traitor? To a land that has already written my name in a different set of books?

**29.4** De Lannoy straightening, looking out through the armoury door at the men drilling in the yard.

> LANNOY: This is my fort now. These are my men.

> LANNOY: If I spend the rest of my life making sure they do not die as stupidly as some of my countrymen did, perhaps that will be enough to balance a few lines.

**29.5** Full width. De Lannoy turned back to Nagoji, the lamp throwing his long shadow across the racks.

> LANNOY: Under whose standard do we truly stand, Ananthan Pillai?

*Page turn.*

---

## PAGE 30

Four panels. The answer. Mirror page 1: the same bastion, the same banner, the men changed. The last panel takes half the page.

**30.1** Two men in the lamplight, the talwar in Nagoji's hand.

> LANNOY: The king's? The idea of this place? The memory of the men who died at Colachel?

> NAGOJI: All of them. On different days.

**30.2** De Lannoy nodding, and then, at Nagoji's answer, smiling.

> LANNOY: On the days when it is the king's, we must be careful. Kings change. Places endure longer.

> NAGOJI: You have been talking to Revathi.

> LANNOY: She scolds me too. Apparently my foreignness does not exempt me.

**30.3** Wide. The two men stepping out onto the wall: De Lannoy taller, bare-headed, pale hair; Nagoji darker, black topknot, silver chain catching the light over his white coat. Below, under the foreigner's tooth, men still drilling in the waning light: Maravar horse and Nair musketeers alike in white coats, Thoma's gun crew at their piece.

> CAPTION: Two men far from the places that had birthed us, bound to a banner that was neither of our first choosing.

> CAPTION: Whatever names future scribes gave this army, for this moment, it was ours.

**30.4** Half the page, final. No figures. The banner staff from below, filling the frame against the last of the light: at the top, the royal standard, red with a silver conch; below it, a smaller pennant, white with a dark blue diagonal line crossed by a dark blue curved line. Both lifting in the evening wind.

> CAPTION: We stood under its standard.

> CAPTION (separate, weighted): Together.

---

## Adaptation notes

- **Page count.** 30 pages and 145 panels against a target of 28 (range 22 to 34). Page counts now vary from three panels to five, with half-page panels for the decision (13.3), Duarte's arrival (15.4) and the final standard (30.4). The extra pages go to the chapter's three dramatic centres: the coat (pages 5 to 14), Father Duarte (pages 15 to 20) and the heir (pages 21 to 26). The opening exposition and the Thoma and Avraham material pay for it.
- **Opening exposition compressed to four pages.** The chiefs who delay their levies, the sharper questions about levy structures and the officers' tightened mouths become one caption over a gap-toothed drill line (2.3). Lannoy's answer "We fight so that whoever sits on that platform cannot easily undo what we have built" is kept, over a full-width view of the palace roofs, so "a selfish defence" says what is selfish. "There you go with your unpleasant truths again" is cut; the Senior Rani's line at 24.4 stands on its own. Ibrahim's new flags and Padmini's "more than one kind of jaw" share one panel (4.1).
- **"I have served you in the clothes I brought from the Deccan"** becomes "in my own clothes" (7.3). CONTINUITY.md dresses him as Ananthan Pillai in mundu and topknot from chapter 17, so the novel's wording would contradict the art.
- **The Goa officer** is not in the chapter 1 to 3 scripts. He appears only in stains, framed at the chin so his eyes are never shown, as a pale European whose coat has a different cut and ornate gilt buttons, as the novel says ("the buttons plain rather than ornate"). Portuguese soldiers in white and red walk the corridor in 6.5, drawn white-dominant so they do not read as redcoats; the gaol guards stay in buff jerkins and morions to match chapter 2. "Blood on the floor" is kept as speech, but the floor is never shown (11.2). The cell in 11.3 has empty manacles on a chain, not a rope, because the novel says he "hung from the chains". Nagoji's cuff gesture in 14.3 mirrors 11.1 on purpose, with plain buttons and a brown hand.
- **Captions that would describe the art were cut.** "My throat tightened" is the silent close on his throat (7.1), which now carries the novel's "The coat was not Portuguese" instead. "The others filed out. I stayed" is 7.5. The novel's one-word paragraph "Fear" is carried by Duarte's face in 16.4, with the caption stopping at "something I had not expected." The sequence of Duarte's expressions is drawn as three slices (16.3), not listed.
- **Chapter 1 and 2 plants paid off.** Duarte's nod (16.1, echoing ch1 8.2), the wrist grab at the brazier (19.2, echoing ch1 8.5) and the slow sign of the cross (19.3, echoing ch2 2.4). Each stain is described in full, since the image model cannot see the earlier chapters. Lannoy's "Dead men cannot testify" (9.3) is kept word for word with its reason, because it echoes Duarte's "A dead prisoner cannot testify" in chapter 1.
- **Cut from the Duarte scene:** "You were right about one thing... the men who fight become something they did not expect," because "The man you tortured is gone" carries the same turn in fewer words; and "Sign whatever treaties Ramayyan puts in front of you," trimmed to "tell them what you saw here." The coat-on-its-peg image that night is folded into the walk away from Duarte (20.5), which carries "But it was smaller."
- **The heir.** His wound is kept specific: he froze at the great temple while his uncle bled for him. The memory is a bloodless daylight stain of the chapter 23 attack (21.3) lettered "The King's blood on white silk"; he names it at dawn ("If my uncle had not...", 25.2); and it pays off at 26.3 ("The one who stood there while others bled for him"). Ramayyan's exchange is cut down to two lines and the page turn "The Senior Rani has concerns" (22.5). "Then teach him your accounts" is cut. The Senior Rani keeps the coin, the line and the threat, but loses "Four hundred years of women" and "a woman who had learned to carry weight"; the art carries her walk. Also cut: the Prince's "dangerous woman" exchange, the palanquin and Pillamar horse lore, the Revathi-like smile (drawn, not named), and the third-month exchange on De Lannoy calling Nagoji too hard ("I have my own wars").
- **Thoma and Avraham** (three sections, about 1,500 words) are compressed to two pages. Neither recurs in chapters 25 to 28. Cut: the Dutch foundry lesson, the Malabari and Paradesi distinction, Ladino, trade routes to Basra and Amsterdam, Avraham's "You are early" and "The roads from Kochi are clear", and "Survive first. Remember always." Thoma's "This coast has buried empires before them" now sets up "their coats", and the page turns on Nagoji's challenge so "That is not surrender. That is wisdom" answers it overleaf.
- **Continuity.** Nagoji is in topknot, mundu and silver chain until the coats arrive (14.2), and in the white coat, red waistcoat, plain brass buttons and buckled riding boots from then on, with the silver chain of office worn over the coat, as the chapter 25 script (1.1) has it. His chin is clean-shaven and his moustache thick throughout. Every Nagoji panel on pages 1 to 13 restates that he is not yet in uniform, because the injected CONTINUITY row says "Ch24 onward in uniform" (see the cast notes; the author should amend that row). No soldier wears a coat before page 14. Lannoy is in the white Travancore coat from page 1, because the king says "He wears the coat already." The Prince is about fourteen. Duarte is older and greyer in the present and dark-haired in the stains, never with a collar tab. Kayal follows the chapter 14 and 22 scripts. The standard and pennant are described in the same words at 1.1, 1.4 and 30.4.
- **Cast overrides** (`scripts/CHAPTER-24-CAST-OVERRIDES.json`) keep Nagoji's chapter 24 sheet off the panels where he is absent or in another period: the Goa stains, the Duarte stains, the temple stain, the drill seen from the bastion, and the pennant close-ups.
- **Verbatim lines kept:** "Better a tooth than a sore," "Preventable deaths exhaust me," "Selfish defence keeps people alive," "Complicated," "Not a rabble. A machine," "Hesitation kills," "The coat was not Portuguese," "Knowing and feeling are different animals," "Ask him how it sits on a man who once wore a different one," "Dead men cannot testify," "The coat is simply the weaving," "I see the door closing behind him while I hung from the chains," "wrong *together*," "we fight as one," "You have the same choice," "You make it sound simple," "Eventually, the glass becomes smaller," "The same drills. Different cloth. Mount up," "Most of it was. I did not," "It seems you found the better powder," "It would not be unjust," "The slow one. The one that asks for something," "I wear this coat now. I drill these men," "The man you tortured is gone," "But it was smaller," "How to stay alive when men want me dead," "The King's blood on white silk," "A mother's fear can become a son's chains," "Not a soldier. Not a prince. A line," "He did. That is what matters," "You speak through it," "You will never be that boy again," "Then I will try to enjoy the burning," "This coast has buried empires before them. It will bury more," "All allies are strange. Until you need them," "All of them. On different days," "Kings change. Places endure longer," and the last word, "Together."
- **Print.** Every widescreen panel is drawn with no text in the art and blank reserves for lettering. Each placed frame must reach 300 PPI or more at its printed size (6x9 in trim plus bleed), and is upscaled 2x or regenerated if it falls short, as CONTINUITY.md requires.

### Review changes

- **Coat argument restored (pages 12 and 13).** Lannoy's "That is what the coat means... we fight as one", the challenge "You have the same choice... could not see past his scars", Nagoji's caption "The words struck harder than I wanted to admit" and "You make it sound simple" are back. Page 12 ends on that pushback; "It is not simple" opens page 13, and the decision gets half a page with a single Keshavrao stain. 12.1 and 13.1 to 13.2 are now under 45 words each ("I still wake up speaking Flemish" is cut).
- **The Prince's wound restored (21.3, 25.2 to 25.3, 26.2 to 26.3).** "The King's blood on white silk" over a daylight stain of the chapter 23 attack; "If my uncle had not..." / "He did. That is what matters."; and "The one who stood there while others bled for him" / "You will never be that boy again." The Senior Rani's line drops its repeated "when the chaver came" (23.5).
- **Other novel lines restored:** the full "hung from the chains" line (11.4); "I knew too much about their failures" (9.3); "We fight so that whoever sits on that platform..." (2.5); "Others died in your cells" and "I wear this coat now. I drill these men" (20.1 to 20.2); Thoma's "history began when their ships arrived" (27.5); "The coat was not Portuguese... plain rather than ornate" (7.1).
- **Duarte's confrontation** is said face to face (20.4) before Nagoji walks away (20.5). The move toward the cross happens once (17.3); in 16.4 his hand twitches in his sleeve. 18.5 is Nagoji alone, and the head shake opens 19.1.
- **Page turns and endings:** page 2 ends on "Selfish defence keeps people alive" over the palace roofs; page 3 ends on the recruit and "which title"; page 13 on "I will wear it"; page 27 on "And yet we wear their coats now"; page 29 on the title question; page 30 on the standard alone, with no figures, under "We stood under its standard" / "Together."
- **Pacing and layout:** panel counts vary (pages 9, 15 and 30 have four panels, page 13 has three), with half-page panels at 13.3, 15.4 and 30.4. Pages 9 to 13 give each panel business and a new angle, and the light moves from sunset to dusk to last light to the first lamps. Pages 4 and 17 give Revathi and Duarte hands and props. The armoury is set at evening (29.1) to match the waning light on the wall.
- **Captions that narrated the art were trimmed:** 6.4, 14.2, 14.3, 16.1, 16.2, 21.1, 22.4, 25.1; the thesis caption on 3.5 is cut. Word counts trimmed at 2.3, 3.1, 6.2, 7.3.
- **Continuity:** a cast and look block at the top; a "not yet in uniform" line in every Nagoji panel on pages 1 to 13; pre-uniform dress for all troops before page 14; the Goa officer as a pale European with a different cut and ornate buttons; both prisoners named and dressed in 6.5; empty manacles instead of a rope (11.3); João's sleeve and a younger Duarte spelled out in the stains (16.1, 19.2, 19.3); anchors to tell Nagoji from the Nair officers, De Lannoy and the Prince in group and hands-only panels (5.1, 6.4, 7.5, 14.4, 15.1, 26.1, 29.2, 30.3); the red conch standard and a fixed pennant description (1.1, 1.4, 30.4); the full uniform with silver chain and boots (14.2); a healed palm scar (24.2); per-frame generation for the repeated faces (16.3, 22.4); no priest or altar wording (27.4); betel teeth instead of "grinning red" (27.5); and a cast overrides file.
- **Stains reduced.** The Colachel stain in 9.3 is cut (it was Lannoy's memory, not Nagoji's), and 13.3 keeps one stain instead of four.
