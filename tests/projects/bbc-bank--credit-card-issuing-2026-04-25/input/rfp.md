---
type: apv-meta
category: rfp-document
title: "Converted from BBC Questionnaire.xlsx"
created: 2026-04-25 09:08
tags: [apv, rfp, converted, markitdown]
source_file: BBC Questionnaire.xlsx
---

## Questionnaire
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 |
| --- | --- | --- | --- |
| No. | Question | NaN | Answers |
| Applications List | NaN | NaN | NaN |
| 1 | Applications Form ( for customer onbording ) | Does the bank already have an application form system used for other products? Is it expected to use the same system, or will it still use a manual data entry method by employees? | Branch staff will do Manual Key-in , PaySuit Noneed to interface with Applications Form for this phase |
| 2 | Origination/Credit Scoring | Does the bank already have an Origination system that includes credit scoring? What is the credit scoring methodology and how does it connect to obtain the score? If a system already exists, is it expected to be used interchangeably, or will data analysis be performed by employees? | BCC will utilize existing system , Branch staff will do Manual Key-in , PaySuit No Need to interface with Applications Form for this phase |
| 3 | Fraud | Does the bank already have a fraud prevention system in place for other products? Is it expected to use the same system? What method will be used for the connection? | Propose with PSS standard Fraud |
| 4 | Collection | Does the bank already have a collection system used for other products? Is it expected to use the same system? What method will be used for the connection? | Propose with PSS standard Collection |
| 5 | Mobile Application | Does the bank already have a mobile application? Does the credit card system need to be connected to the mobile application? If so, how? | This phase not include mobile application but in future need to integration with mobile application m PSS need to provide API |
| 6 | BI Dashboard/Report Portal | Does the bank already have a BI Dashboard/Report Portal? Does the credit card system need to be connected to the BI Dashboard/Report Portal? If so, how? | Bank not specific BI Dashboard/Report Portal , CNN can propose with PSS Standard Report and Dashboard in PSS web portal/backend portal |
| 7 | Loyalty | Does the bank already have a loyalty system in place for other products? Is it expected to use the same system? What method will be used for the integration? | This phase focus on Core System and issue only plastic card , for loyalty can be next phase |
| 8 | ACS | Does the bank already have an ACS system? Is it expected to use the same system or will it acquire a new one? | This phase focus on Core System and issue only plastic card , for Online transaction or ACS can be next phase |
| 9 | KYC | Does the bank already have a KYC system? Is it expected to use the same system or will a new one be procured? | BCC will utilize existing system , Branch staff will do Manual Key-in , PaySuit No Need to interface with KYC for this phase |
| 10 | Card Embossing | Does the bank has ready embossing system to print credit card? | Currently BCC has printing company who print ATM card , BCC will utilize existing vendor , Currently BCC send embossing file to vendor via Email and FTP |
| 11 | Card Statement generator | Does the bank has ready statement printer/generator to print credit card statement? | Currently BCC has printing company who print ATM card , BCC will need to check with them in case need to print statement |
| 12 | Charges/Pricing | Does the bank has standalone pricing module or we can use the base offering from PSS? | Propose with PSS standard Fraud |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN |
| Hardware List | NaN | NaN | NaN |
| 1 | HSM | Does the bank already use its own HSM (High-Speed ​​Margin)? Is it expected to use the same system or looking a new one? | BBC expected CNN will proposed solution with SaaS model , should include in CNN SaaS service |
| 2 | Gateway (VISA/MasterCard) | Does the bank already use its own VISA Gateway? | BBC expected CNN will proposed solution with SaaS model , should include in CNN SaaS service, This phase foe VISA only |
| NaN | NaN | NaN | NaN |
| No. | Question | NaN | NaN |
| Report /Interface | NaN | NaN | NaN |
| 1 | BOL Report | How many report for BOL , Please share report list (If Any) | BBC will share Report List / Number of Report (CNN can estimate with assumption i.e. Share PSS Standard report and Customization Report Maximum xxx Reports ) |
| 2 | Internal/External | How many specific report for internal/External (If Any) | BBC will share System List for integration (CNN can estimate with assumption i.e. Maximum xxx APIs ) |
| 3 | Interface | How many interface with Credit Card System , How to interface ,Please share report list (If Any) | PaySuit need to interface with Mobile, Internet ,core banking but this phase focuse Core System first , CNN can propose with minimum that PSS need to interface (CNN can estimate with assumption i.e. Maximum xxx APIs ) |
| NaN | NaN | NaN | NaN |
| No. | Question | NaN | NaN |
| Card Product | NaN | NaN | NaN |
| 1 | Credit | Does the system need to support credit card issuance? | Implement Credit Card First Phase with 3 Type of card (Classic,Gold,Platinum) |
| 2 | Debit | Does the system need to support issuing debit cards? | Implement Credit Card First Phase , Debit Card next phase |
| 3 | Prepaid | Does the system need to support issuing prepaid cards? | Implement Credit Card First Phase , Prepaid Card next phase |
| 4 | Travel | Does the system need to support the issuance of Travel cards? | Implement Credit Card First Phase , No plan for Travel |
| 5 | Fleet Card | Does the system need to support the issuance of Fleet Cards? | Implement Credit Card First Phase , No plan for Fleet Card |
| 6 | Corporate Card | Does the system need to support the issuance of corporate cards? | Implement Credit Card First Phase , No plan for Corporate Card |
| 7 | Revolving card | Does the system need to support issuing Revolving cards? | Implement Credit Card First Phase , No plan for Revolving card |
| 8 | Personal loan | Does the system need to support the issuance of personal loan cards? | Implement Credit Card First Phase , No plan for Personal loan |
| NaN | NaN | NaN | NaN |
| No. | Question | NaN | NaN |
| Card Type | NaN | NaN | NaN |
| 1 | Magnetic | Does the system need to support the issuance of magnetic cards? | Yes, Should follow VISA Standard |
| 2 | Chip /EMV | Does the system need to support chip/EMV card issuance? | Yes, Should follow VISA Standard |
| 3 | Contactless | Does the system need to support contactless card issuance? | Yes, Should follow VISA Standard |
| 4 | Tokenization | Does the system need to support tokenization for card issuance? | This phase focus on plastic card , Tokenization can be Next phase |
| 5 | Chip-and-signature | Does the system need to support chip-and-signature card issuance? | Yes, Should follow VISA Standard |
| 6 | Chip-and-PIN | Does the system need to support chip-and-PIN card issuance? | Yes, Should follow VISA Standard |
| 7 | DCC | Does the system need to support DCC card issuance? | Yes, Should follow VISA Standard |
| 8 | Dynamic CVV | Does the system need to support issuing Dynamic CVV cards? | Can be Next Phase |
| 9 | QR Code (Card Scheme) | Does the system need to support VISA QR Payment? | This phase focus on plastic card , QR Payment can be Next phase |
| 10 | Plastic Card | Does the system need to support the issuance of plastic cards? | This phase focus on plastic card, Should follow VISA Standard |
| 11 | Virtual Card | Does the system need to support the issuance of virtual cards? | This phase focus on plastic card , Virtual can be Next phase |
| NaN | NaN | NaN | NaN |
| No. | Question | NaN | NaN |
| Performance | NaN | NaN | NaN |
| 1 | Ability to support concurrent users | How many concurrent users must the system be able to support, and what is the maximum number of users it can support? | CNN can propose with CNN Standard SaaS |
| 2 | Ability to support RTO | What is the required RTO ? | CNN can propose with CNN Standard SaaS |
| 3 | Ability to support RPO | What is the required RPO ? | CNN can propose with CNN Standard SaaS |
| 4 | Ability to support SLA | What SLA (Service Level Agreement) requirements does the system need to support, and how does it need to support each SLA level? Is SLA sharing possible? | CNN can propose with CNN Standard SaaS |
| 5 | Number of User | How many users are currently using the screen? How many users are expected to be supported in the future? | 20 User |
| NaN | NaN | NaN | NaN |
| No. | Question | NaN | NaN |
| Payment Service | NaN | NaN | NaN |
| 1 | Sale | Does the system need to support sale transactions? | Yes, Should follow VISA Standard |
| 2 | Cash advance | Does the system need to support cash advance transactions? | Yes, Should follow VISA Standard |
| 3 | Installment | Does the system need to support installment transactions? | Can be Next phase |
| 4 | Online redemption | Does the system need to support online redemption? | Can be Next phase |
| 5 | Recurring | Does the system need to support recurring transactions? | Yes, Should follow VISA Standard |
| NaN | NaN | NaN | NaN |
| No. | Question | NaN | NaN |
| Forcecast | NaN | NaN | NaN |
| 1 | Number of Application Year 1 | Estimated number of applications in year 1. | Not include LOS , not required this information |
| 2 | Number of Application Year 2 | Estimated number of applications in year 2. | Not include LOS , not required this information |
| 3 | Number of Application Year 3 | Estimated number of applications in year 3. | Not include LOS , not required this information |
| 4 | Number of Application Year 4 | Estimated number of applications in year 4. | Not include LOS , not required this information |
| 5 | Number of Application Year 5 | Estimated number of applications in year 5. | Not include LOS , not required this information |
| 6 | Number of Card Year 1 | Projected number of cards issued in year 1. | BBC will share via email |
| 7 | Number of Card Year 2 | Projected number of cards issued in year 2. | BBC will share via email |
| 8 | Number of Card Year 3 | Projected number of cards issued in year 3. | BBC will share via email |
| 9 | Number of Card Year 4 | Projected number of cards issued in year 4. | BBC will share via email |
| 10 | Number of Card Year 5 | Projected number of cards issued in year 5. | BBC will share via email |
| 11 | Number of Transaction Year 1 | Projected number of Transaction in year 1. | BBC will share via email |
| 12 | Number of Transaction Year 2 | Projected number of Transaction in year 2. | BBC will share via email |
| 13 | Number of Transaction Year 3 | Projected number of Transaction in year 3. | BBC will share via email |
| 14 | Number of Transaction Year 4 | Projected number of Transaction in year 4. | BBC will share via email |
| 15 | Number of Transaction Year 5 | Projected number of Transaction in year 5. | BBC will share via email |
| NaN | NaN | NaN | BBC will share via email |

## Sheet1
|
|  |
---

---
type: apv-meta
category: rfp-document
title: "Converted from BBC Bank Card Volume.xlsx"
created: 2026-04-25 09:08
tags: [apv, rfp, converted, markitdown]
source_file: BBC Bank Card Volume.xlsx
---

## Sheet1
| Card Voluume | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Card type | Product | Y1 | Y2 | Y3 | Y4 | Y5 |
| End Cards | Debit | Platinium | 1000 | 1100 | 1300 | 1500 | 1700 |
| NaN | Debit | Classic | 7000 | 7700.0 | 8500 | 9500 | 10500 |
| NaN | Credit | Infinite | 200 | 250 | 300 | 350 | 400 |
| NaN | Credit | Platinium | 800 | 1000 | 1300 | 1500 | 1700 |
| NaN | Credit | Classic | 1200 | 1500 | 1700 | 2000 | 2300 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| 1. End Cards = target number of cards at end of year | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | Card type | Product | Y1 | Y2 | Y3 | Y4 | Y5 |
| Payment Volume (PV) per card | Debit | Platinium | 1000 | 1200 | 1440 | 1728 | 2073.6 |
| NaN | Debit | Classic | 500 | 600 | 720 | 864 | 1036.8 |
| NaN | Credit | Infinite | 5000 | 6000 | 7200 | 8640 | 10368 |
| NaN | Credit | Platinium | 2000 | 2400 | 2880 | 3456 | 4147.2 |
| NaN | Credit | Classic | 1000 | 1200 | 1440 | 1728 | 2073.6 |
| NaN | 0 | 0 | NaN | NaN | NaN | NaN | NaN |
| NaN | 0 | 0 | NaN | NaN | NaN | NaN | NaN |
| NaN | 0 | 0 | NaN | NaN | NaN | NaN | NaN |