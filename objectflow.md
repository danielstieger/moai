# Objectflow

- Modellierung von Datenstrukturen, Geschäftslogik, Abläufe & Ui-Steuerung und Querschnittsbelange

# Zentrale Themen

- Datenstrukturen Entity / Value Object und DTO, verwendbare Felder mit Typen, Status spezielles Konzept und Umgang mit string (Klein! nicht java.String) und BigDezimalsupport (im mps als 13.44bd)
- Commands, Typen & Page mit done, precondition, page xxx etc. FINAL_CONCLUSION Logik (default & action parameterisierung getSelected() [+ derived ist interessant] getSelectedObjects() und der Einfluss auf Command-Enabled, session merge und roundtrips SEARCH COMMAND - GO und aktualisierung SEARCH.  
- session handling und Konzepte zum session zugriff, auch getUserEnv() und getUserService(), Warum check-in und check-out logik, warum session operations stack? 
- Was hat es mit dem successor / predecessor command auf sich? 
- meta-info mit # und ui steuerung
- permissions und roles konzept von objectflow und möglichkeiten
- Besonders wichtig! Services (Zustandslos)/ Servicemethoden + der OperationCall + precondition/validation in services möglich, Großes Todo im allgemeinen, Zustandübergänge modellieren in Services und generell, was soll in services modelliert. Services ist ja super zentral!
- String support mit dem Konzept org.modellwerkstatt.objectflow.structure.StringFormatString (impl. org.modellwerkstatt.objectflow.runtime.OFXStringFormatter2)
- observability (Implementierung in org.modellwerkstatt.dataux.runtime.core.ApplicationReporter, impl nicht dokumentieren nur für verständnis) und log-statement 
- static ressources und möglichkeiten 
- configuration mit OFXConfig, konzeptionell eigentlich spring ioc mit xml dahinter 
- testing mit eigener Test-Suit und das run command zum ausführen von commands ohne ui!
- serdes möglichkeiten (org.modellwerkstatt.objectflow.serdes.CONV) [implementierung zum nachschlagen in org.modellwerkstatt.objectflow.sdservices, impl. nicht dokumentieren]
