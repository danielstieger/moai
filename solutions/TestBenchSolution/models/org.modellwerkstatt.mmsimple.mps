<?xml version="1.0" encoding="UTF-8"?>
<model ref="r:6a0f20ce-97c0-4695-90b8-29c244e60745(org.modellwerkstatt.mmsimple)">
  <persistence version="9" />
  <languages>
    <use id="ec097fca-5b84-41f2-847d-6a5690cae277" name="org.modellwerkstatt.objectflow" version="0" />
    <use id="f3061a53-9226-4cc5-a443-f952ceaf5816" name="jetbrains.mps.baseLanguage" version="12" />
    <use id="5aaa957f-3447-4783-b1f7-b301fa3e0394" name="org.modellwerkstatt.manmap" version="0" />
    <use id="83888646-71ce-4f1c-9c53-c54016f6ad4f" name="jetbrains.mps.baseLanguage.collections" version="2" />
    <devkit ref="b2950e54-da96-4c3b-868c-2b5e12af9605(org.modellwerkstatt.MoWareWerkbank)" />
  </languages>
  <imports>
    <import index="wyt6" ref="6354ebe7-c22a-4a0f-ac54-50b52ab9b065/java:java.lang(JDK/)" />
    <import index="w08f" ref="37fdf88a-1025-4d01-864a-0bf987f72e6f/java:org.joda.time(org.modellwerkstatt.manmap.runtime/)" />
    <import index="xlxw" ref="6354ebe7-c22a-4a0f-ac54-50b52ab9b065/java:java.math(JDK/)" />
  </imports>
  <registry>
    <language id="f3061a53-9226-4cc5-a443-f952ceaf5816" name="jetbrains.mps.baseLanguage">
      <concept id="1201370618622" name="jetbrains.mps.baseLanguage.structure.Property" flags="ig" index="2RhdJD">
        <property id="1201371481316" name="propertyName" index="2RkwnN" />
        <child id="1201371521209" name="type" index="2RkE6I" />
        <child id="1201372378714" name="propertyImplementation" index="2RnVtd" />
      </concept>
      <concept id="1201372606839" name="jetbrains.mps.baseLanguage.structure.DefaultPropertyImplementation" flags="ng" index="2RoN1w">
        <child id="1202065356069" name="defaultGetAccessor" index="3wFrgM" />
        <child id="1202078082794" name="defaultSetAccessor" index="3xrYvX" />
      </concept>
      <concept id="1137021947720" name="jetbrains.mps.baseLanguage.structure.ConceptFunction" flags="in" index="2VMwT0">
        <child id="1137022507850" name="body" index="2VODD2" />
      </concept>
      <concept id="1070475926800" name="jetbrains.mps.baseLanguage.structure.StringLiteral" flags="nn" index="Xl_RD">
        <property id="1070475926801" name="value" index="Xl_RC" />
      </concept>
      <concept id="1070534370425" name="jetbrains.mps.baseLanguage.structure.IntegerType" flags="in" index="10Oyi0" />
      <concept id="1068390468198" name="jetbrains.mps.baseLanguage.structure.ClassConcept" flags="ig" index="312cEu">
        <property id="4980874121082273661" name="isStatic" index="3n5e7y" />
      </concept>
      <concept id="1068498886296" name="jetbrains.mps.baseLanguage.structure.VariableReference" flags="nn" index="37vLTw">
        <reference id="1068581517664" name="variableDeclaration" index="3cqZAo" />
      </concept>
      <concept id="1068498886292" name="jetbrains.mps.baseLanguage.structure.ParameterDeclaration" flags="ir" index="37vLTG" />
      <concept id="1225271177708" name="jetbrains.mps.baseLanguage.structure.StringType" flags="in" index="17QB3L" />
      <concept id="4972933694980447171" name="jetbrains.mps.baseLanguage.structure.BaseVariableDeclaration" flags="ng" index="19Szcq">
        <child id="5680397130376446158" name="type" index="1tU5fm" />
      </concept>
      <concept id="1068580123132" name="jetbrains.mps.baseLanguage.structure.BaseMethodDeclaration" flags="ng" index="3clF44">
        <child id="1068580123133" name="returnType" index="3clF45" />
        <child id="1068580123134" name="parameter" index="3clF46" />
        <child id="1068580123135" name="body" index="3clF47" />
      </concept>
      <concept id="1068580123155" name="jetbrains.mps.baseLanguage.structure.ExpressionStatement" flags="nn" index="3clFbF">
        <child id="1068580123156" name="expression" index="3clFbG" />
      </concept>
      <concept id="1068580123136" name="jetbrains.mps.baseLanguage.structure.StatementList" flags="sn" stub="5293379017992965193" index="3clFbS">
        <child id="1068581517665" name="statement" index="3cqZAp" />
      </concept>
      <concept id="1068580123140" name="jetbrains.mps.baseLanguage.structure.ConstructorDeclaration" flags="ig" index="3clFbW" />
      <concept id="1068581517677" name="jetbrains.mps.baseLanguage.structure.VoidType" flags="in" index="3cqZAl" />
      <concept id="1107461130800" name="jetbrains.mps.baseLanguage.structure.Classifier" flags="ng" index="3pOWGL">
        <property id="1211504562189" name="nestedName" index="jj94n" />
        <child id="5375687026011219971" name="member" index="jymVt" unordered="true" />
      </concept>
      <concept id="1107535904670" name="jetbrains.mps.baseLanguage.structure.ClassifierType" flags="in" index="3uibUv">
        <reference id="1107535924139" name="classifier" index="3uigEE" />
      </concept>
      <concept id="1202065242027" name="jetbrains.mps.baseLanguage.structure.DefaultGetAccessor" flags="ng" index="3wEZqW" />
      <concept id="1202077725299" name="jetbrains.mps.baseLanguage.structure.DefaultSetAccessor" flags="ng" index="3xqBd$">
        <child id="1202077744034" name="visibility" index="3xqFEP" />
      </concept>
      <concept id="1178549954367" name="jetbrains.mps.baseLanguage.structure.IVisible" flags="ngI" index="1B3ioH">
        <child id="1178549979242" name="visibility" index="1B3o_S" />
      </concept>
      <concept id="1146644602865" name="jetbrains.mps.baseLanguage.structure.PublicVisibility" flags="nn" index="3Tm1VV" />
    </language>
    <language id="ec097fca-5b84-41f2-847d-6a5690cae277" name="org.modellwerkstatt.objectflow">
      <concept id="6525155817176738379" name="org.modellwerkstatt.objectflow.structure.PageInitConceptFunc" flags="ig" index="20qEzJ" />
      <concept id="1707086779731223260" name="org.modellwerkstatt.objectflow.structure.OnCreationStatusElemOption" flags="ng" index="2_5uyX" />
      <concept id="4533072425307715670" name="org.modellwerkstatt.objectflow.structure.StatusElement" flags="ng" index="2XvgOc">
        <property id="4533072425307715682" name="value" index="2XvgOS" />
        <child id="1707086779727598829" name="options" index="2_RhUc" />
        <child id="6436022531938294753" name="shortDescNew" index="3RLGe5" />
        <child id="6436022531938294806" name="longDescNew" index="3RLGhM" />
      </concept>
      <concept id="4533072425307715669" name="org.modellwerkstatt.objectflow.structure.StatusDeclaration" flags="ng" index="2XvgOf">
        <child id="4533072425307715672" name="element" index="2XvgO2" />
      </concept>
      <concept id="4533072425307800381" name="org.modellwerkstatt.objectflow.structure.StatusType" flags="ig" index="2XvVpB">
        <reference id="6600213247848012755" name="status" index="3$lB4D" />
      </concept>
      <concept id="3887124829264538773" name="org.modellwerkstatt.objectflow.structure.PagePaneActionProviderLink" flags="ng" index="3063JU" />
      <concept id="4313579457188683399" name="org.modellwerkstatt.objectflow.structure.IOFXObject" flags="ngI" index="13YVsI">
        <child id="3207218222495905601" name="businessProperties" index="TxmiU" />
      </concept>
      <concept id="1372017518093514468" name="org.modellwerkstatt.objectflow.structure.Entity" flags="ig" index="34Athd">
        <child id="4533072425307746563" name="status" index="2XvChp" />
      </concept>
      <concept id="8396343267227475961" name="org.modellwerkstatt.objectflow.structure.BusinessProperty" flags="ig" index="1bOX9e">
        <child id="3674496190757459099" name="propertyOption" index="0orDa" />
        <child id="5770301300929026308" name="longDesc" index="2CNmdL" />
        <child id="5770301300929026304" name="shortDesc" index="2CNmdP" />
      </concept>
      <concept id="7192042020163999178" name="org.modellwerkstatt.objectflow.structure.Command" flags="ng" index="3ugp7m">
        <property id="1001479520354727786" name="newWindowTitleType" index="1ptSWV" />
        <child id="7192042020164064743" name="pages" index="3ug97V" />
      </concept>
      <concept id="7192042020163999174" name="org.modellwerkstatt.objectflow.structure.PageCrtl" flags="ng" index="3ugp7q">
        <child id="3887124829264538806" name="pagePaneActionProviderLink" index="3063Jp" />
        <child id="1881524139084590808" name="pageInit" index="10qiF$" />
      </concept>
    </language>
    <language id="5aaa957f-3447-4783-b1f7-b301fa3e0394" name="org.modellwerkstatt.manmap">
      <concept id="774207833082573402" name="org.modellwerkstatt.manmap.structure.QueryFromMap" flags="ng" index="jybIQ">
        <property id="3572493221071471725" name="readOnly" index="HScZ5" />
        <child id="774207833082779687" name="queryOperation" index="jxX7b" />
      </concept>
      <concept id="774207833082448725" name="org.modellwerkstatt.manmap.structure.OptimisticOption" flags="ng" index="jyGaT" />
      <concept id="774207833082557389" name="org.modellwerkstatt.manmap.structure.KeyOption" flags="ng" index="jyRCx" />
      <concept id="774207833082557394" name="org.modellwerkstatt.manmap.structure.AutoidOption" flags="ng" index="jyRCY">
        <child id="774207833082557396" name="sequenceName" index="jyRCS" />
      </concept>
      <concept id="4421815423107469587" name="org.modellwerkstatt.manmap.structure.Repository" flags="ig" index="DXQ2w" />
      <concept id="4421815423107469588" name="org.modellwerkstatt.manmap.structure.RepositoryInstanceMethodDeclaration" flags="ig" index="DXQ2B">
        <property id="8796175910513646269" name="repoMethodType" index="2a4t7v" />
      </concept>
      <concept id="8172309840348950202" name="org.modellwerkstatt.manmap.structure.INeedsClassMapper" flags="ngI" index="P14SU">
        <reference id="8172309840348950203" name="entityMapping" index="P14SV" />
      </concept>
      <concept id="8172309840348863378" name="org.modellwerkstatt.manmap.structure.SaveWithMap" flags="ng" index="P1rGi">
        <child id="8172309840348863385" name="expression" index="P1rGp" />
      </concept>
      <concept id="6435836305144935126" name="org.modellwerkstatt.manmap.structure.GetQuery" flags="ng" index="TUlRj">
        <child id="6435836305144935143" name="argument" index="TUlRy" />
      </concept>
      <concept id="871579071900124823" name="org.modellwerkstatt.manmap.structure.PersistenceDescription" flags="ng" index="12nvSr">
        <child id="871579071900209328" name="persistenceMapping" index="12nEwW" />
      </concept>
      <concept id="871579071900209258" name="org.modellwerkstatt.manmap.structure.EntityMapping" flags="ng" index="12nEzA">
        <reference id="871579071900233967" name="classConcept" index="12nOxz" />
        <child id="774207833082448730" name="tableOption" index="jyGaQ" />
        <child id="871579071901472001" name="tableName" index="12gAQd" />
      </concept>
      <concept id="871579071900209251" name="org.modellwerkstatt.manmap.structure.FieldMapping" flags="ng" index="12nEzJ">
        <reference id="871579071900248751" name="property" index="12nL8z" />
        <child id="871579071900290535" name="fieldName" index="12k7lF" />
      </concept>
      <concept id="871579071900248872" name="org.modellwerkstatt.manmap.structure.IMapsClassConcept" flags="ngI" index="12nLe$">
        <child id="4557816287827057767" name="atomMpig" index="3caO6$" />
      </concept>
      <concept id="781751828139414632" name="org.modellwerkstatt.manmap.structure.NoKeyMapperField" flags="ng" index="1o6$dd" />
    </language>
    <language id="ceab5195-25ea-4f22-9b92-103b95ca8c0c" name="jetbrains.mps.lang.core">
      <concept id="1133920641626" name="jetbrains.mps.lang.core.structure.BaseConcept" flags="ng" index="2VYdi">
        <property id="1193676396447" name="virtualPackage" index="3GE5qa" />
      </concept>
      <concept id="1196978630214" name="jetbrains.mps.lang.core.structure.IResolveInfo" flags="ngI" index="2Lv6Xg">
        <property id="1196978656277" name="resolveInfo" index="2Lvdk3" />
      </concept>
      <concept id="1169194658468" name="jetbrains.mps.lang.core.structure.INamedConcept" flags="ngI" index="TrEIO">
        <property id="1169194664001" name="name" index="TrG5h" />
      </concept>
    </language>
    <language id="83888646-71ce-4f1c-9c53-c54016f6ad4f" name="jetbrains.mps.baseLanguage.collections">
      <concept id="1151688443754" name="jetbrains.mps.baseLanguage.collections.structure.ListType" flags="in" index="_YKpA">
        <child id="1151688676805" name="elementType" index="_ZDj9" />
      </concept>
    </language>
  </registry>
  <node concept="34Athd" id="6qR6GZqdTq8">
    <property role="TrG5h" value="Invoice" />
    <node concept="2XvgOf" id="6qR6GZqdTsJ" role="2XvChp">
      <property role="TrG5h" value="InvoiceStatus" />
      <node concept="2XvgOc" id="6qR6GZqdTsK" role="2XvgO2">
        <property role="TrG5h" value="created" />
        <property role="2XvgOS" value="c" />
        <node concept="Xl_RD" id="6qR6GZqdTsL" role="3RLGe5">
          <property role="Xl_RC" value="created" />
        </node>
        <node concept="Xl_RD" id="6qR6GZqdTsM" role="3RLGhM">
          <property role="Xl_RC" value="created" />
        </node>
        <node concept="2_5uyX" id="6qR6GZqdTsN" role="2_RhUc" />
      </node>
      <node concept="2XvgOc" id="6qR6GZqdTt8" role="2XvgO2">
        <property role="TrG5h" value="signed" />
        <property role="2XvgOS" value="s" />
        <node concept="Xl_RD" id="6qR6GZqdTt9" role="3RLGe5">
          <property role="Xl_RC" value="signed" />
        </node>
        <node concept="Xl_RD" id="6qR6GZqdTta" role="3RLGhM">
          <property role="Xl_RC" value="signed" />
        </node>
      </node>
      <node concept="2XvgOc" id="6qR6GZqdTtn" role="2XvgO2">
        <property role="TrG5h" value="invalid" />
        <property role="2XvgOS" value="i" />
        <node concept="Xl_RD" id="6qR6GZqdTto" role="3RLGe5">
          <property role="Xl_RC" value="invalid" />
        </node>
        <node concept="Xl_RD" id="6qR6GZqdTtp" role="3RLGhM">
          <property role="Xl_RC" value="invalid" />
        </node>
      </node>
    </node>
    <node concept="3Tm1VV" id="6qR6GZqdTqa" role="1B3o_S" />
    <node concept="3clFbW" id="6qR6GZqdTqb" role="jymVt">
      <node concept="3cqZAl" id="6qR6GZqdTqc" role="3clF45" />
      <node concept="3Tm1VV" id="6qR6GZqdTqd" role="1B3o_S" />
      <node concept="3clFbS" id="6qR6GZqdTqe" role="3clF47" />
    </node>
    <node concept="1bOX9e" id="6qR6GZqdTqf" role="TxmiU">
      <property role="2RkwnN" value="id" />
      <property role="TrG5h" value="id" />
      <node concept="3Tm1VV" id="6qR6GZqdTql" role="1B3o_S" />
      <node concept="2RoN1w" id="6qR6GZqdTqm" role="2RnVtd">
        <node concept="3wEZqW" id="6qR6GZqdTqn" role="3wFrgM" />
        <node concept="3xqBd$" id="6qR6GZqdTqo" role="3xrYvX">
          <node concept="3Tm1VV" id="6qR6GZqdTqq" role="3xqFEP" />
        </node>
      </node>
      <node concept="Xl_RD" id="6qR6GZqdTqr" role="2CNmdP">
        <property role="Xl_RC" value="id" />
      </node>
      <node concept="Xl_RD" id="6qR6GZqdTqs" role="2CNmdL">
        <property role="Xl_RC" value="Key-Id" />
      </node>
      <node concept="10Oyi0" id="6qR6GZqdTqt" role="2RkE6I" />
      <node concept="jyRCx" id="6qR6GZqdTqu" role="0orDa" />
      <node concept="jyRCY" id="6qR6GZqdTqv" role="0orDa">
        <node concept="Xl_RD" id="6qR6GZqdTqw" role="jyRCS">
          <property role="Xl_RC" value="S_INVOICE" />
        </node>
      </node>
    </node>
    <node concept="1bOX9e" id="6qR6GZqeRL_" role="TxmiU">
      <property role="2RkwnN" value="invoiceNumber" />
      <property role="TrG5h" value="invoiceNumber" />
      <node concept="Xl_RD" id="6qR6GZqeRLM" role="2CNmdP">
        <property role="Xl_RC" value="Invoice number" />
      </node>
      <node concept="17QB3L" id="6qR6GZqeRSb" role="2RkE6I" />
      <node concept="2RoN1w" id="6qR6GZqeRLO" role="2RnVtd">
        <node concept="3wEZqW" id="6qR6GZqeRLS" role="3wFrgM" />
        <node concept="3xqBd$" id="6qR6GZqeRLT" role="3xrYvX">
          <node concept="3Tm1VV" id="6qR6GZqeRLV" role="3xqFEP" />
        </node>
      </node>
      <node concept="3Tm1VV" id="6qR6GZqeRLW" role="1B3o_S" />
    </node>
    <node concept="1bOX9e" id="6qR6GZqeRLX" role="TxmiU">
      <property role="2RkwnN" value="issueDate" />
      <property role="TrG5h" value="issueDate" />
      <node concept="Xl_RD" id="6qR6GZqeRMa" role="2CNmdP">
        <property role="Xl_RC" value="Issue date" />
      </node>
      <node concept="3uibUv" id="6qR6GZqeRMb" role="2RkE6I">
        <ref role="3uigEE" to="w08f:~LocalDate" resolve="LocalDate" />
      </node>
      <node concept="2RoN1w" id="6qR6GZqeRMc" role="2RnVtd">
        <node concept="3wEZqW" id="6qR6GZqeRMg" role="3wFrgM" />
        <node concept="3xqBd$" id="6qR6GZqeRMh" role="3xrYvX">
          <node concept="3Tm1VV" id="6qR6GZqeRMj" role="3xqFEP" />
        </node>
      </node>
      <node concept="3Tm1VV" id="6qR6GZqeRMk" role="1B3o_S" />
    </node>
    <node concept="1bOX9e" id="6qR6GZqeRMl" role="TxmiU">
      <property role="2RkwnN" value="dueDate" />
      <property role="TrG5h" value="dueDate" />
      <node concept="Xl_RD" id="6qR6GZqeRMy" role="2CNmdP">
        <property role="Xl_RC" value="Due date" />
      </node>
      <node concept="3uibUv" id="6qR6GZqeRMz" role="2RkE6I">
        <ref role="3uigEE" to="w08f:~LocalDate" resolve="LocalDate" />
      </node>
      <node concept="2RoN1w" id="6qR6GZqeRM$" role="2RnVtd">
        <node concept="3wEZqW" id="6qR6GZqeRMC" role="3wFrgM" />
        <node concept="3xqBd$" id="6qR6GZqeRMD" role="3xrYvX">
          <node concept="3Tm1VV" id="6qR6GZqeRMF" role="3xqFEP" />
        </node>
      </node>
      <node concept="3Tm1VV" id="6qR6GZqeRMG" role="1B3o_S" />
    </node>
    <node concept="1bOX9e" id="6qR6GZqeRMH" role="TxmiU">
      <property role="2RkwnN" value="customerName" />
      <property role="TrG5h" value="customerName" />
      <node concept="Xl_RD" id="6qR6GZqeRMU" role="2CNmdP">
        <property role="Xl_RC" value="Customer name" />
      </node>
      <node concept="17QB3L" id="6qR6GZqeRSc" role="2RkE6I" />
      <node concept="2RoN1w" id="6qR6GZqeRMW" role="2RnVtd">
        <node concept="3wEZqW" id="6qR6GZqeRN0" role="3wFrgM" />
        <node concept="3xqBd$" id="6qR6GZqeRN1" role="3xrYvX">
          <node concept="3Tm1VV" id="6qR6GZqeRN3" role="3xqFEP" />
        </node>
      </node>
      <node concept="3Tm1VV" id="6qR6GZqeRN4" role="1B3o_S" />
    </node>
    <node concept="1bOX9e" id="6qR6GZqeRN5" role="TxmiU">
      <property role="2RkwnN" value="billingAddress" />
      <property role="TrG5h" value="billingAddress" />
      <node concept="Xl_RD" id="6qR6GZqeRNi" role="2CNmdP">
        <property role="Xl_RC" value="Billing address" />
      </node>
      <node concept="17QB3L" id="6qR6GZqeRSd" role="2RkE6I" />
      <node concept="2RoN1w" id="6qR6GZqeRNk" role="2RnVtd">
        <node concept="3wEZqW" id="6qR6GZqeRNo" role="3wFrgM" />
        <node concept="3xqBd$" id="6qR6GZqeRNp" role="3xrYvX">
          <node concept="3Tm1VV" id="6qR6GZqeRNr" role="3xqFEP" />
        </node>
      </node>
      <node concept="3Tm1VV" id="6qR6GZqeRNs" role="1B3o_S" />
    </node>
    <node concept="1bOX9e" id="6qR6GZqeRNt" role="TxmiU">
      <property role="2RkwnN" value="netAmount" />
      <property role="TrG5h" value="netAmount" />
      <node concept="Xl_RD" id="6qR6GZqeRNE" role="2CNmdP">
        <property role="Xl_RC" value="Net amount" />
      </node>
      <node concept="3uibUv" id="6qR6GZqeRNF" role="2RkE6I">
        <ref role="3uigEE" to="xlxw:~BigDecimal" resolve="BigDecimal" />
      </node>
      <node concept="2RoN1w" id="6qR6GZqeRNG" role="2RnVtd">
        <node concept="3wEZqW" id="6qR6GZqeRNK" role="3wFrgM" />
        <node concept="3xqBd$" id="6qR6GZqeRNL" role="3xrYvX">
          <node concept="3Tm1VV" id="6qR6GZqeRNN" role="3xqFEP" />
        </node>
      </node>
      <node concept="3Tm1VV" id="6qR6GZqeRNO" role="1B3o_S" />
    </node>
    <node concept="1bOX9e" id="6qR6GZqeRNP" role="TxmiU">
      <property role="2RkwnN" value="taxAmount" />
      <property role="TrG5h" value="taxAmount" />
      <node concept="Xl_RD" id="6qR6GZqeRO2" role="2CNmdP">
        <property role="Xl_RC" value="Tax amount" />
      </node>
      <node concept="3uibUv" id="6qR6GZqeRO3" role="2RkE6I">
        <ref role="3uigEE" to="xlxw:~BigDecimal" resolve="BigDecimal" />
      </node>
      <node concept="2RoN1w" id="6qR6GZqeRO4" role="2RnVtd">
        <node concept="3wEZqW" id="6qR6GZqeRO8" role="3wFrgM" />
        <node concept="3xqBd$" id="6qR6GZqeRO9" role="3xrYvX">
          <node concept="3Tm1VV" id="6qR6GZqeROb" role="3xqFEP" />
        </node>
      </node>
      <node concept="3Tm1VV" id="6qR6GZqeROc" role="1B3o_S" />
    </node>
    <node concept="1bOX9e" id="6qR6GZqeROd" role="TxmiU">
      <property role="2RkwnN" value="totalAmount" />
      <property role="TrG5h" value="totalAmount" />
      <node concept="Xl_RD" id="6qR6GZqeROq" role="2CNmdP">
        <property role="Xl_RC" value="Total amount" />
      </node>
      <node concept="3uibUv" id="6qR6GZqeROr" role="2RkE6I">
        <ref role="3uigEE" to="xlxw:~BigDecimal" resolve="BigDecimal" />
      </node>
      <node concept="2RoN1w" id="6qR6GZqeROs" role="2RnVtd">
        <node concept="3wEZqW" id="6qR6GZqeROw" role="3wFrgM" />
        <node concept="3xqBd$" id="6qR6GZqeROx" role="3xrYvX">
          <node concept="3Tm1VV" id="6qR6GZqeROz" role="3xqFEP" />
        </node>
      </node>
      <node concept="3Tm1VV" id="6qR6GZqeRO$" role="1B3o_S" />
    </node>
    <node concept="1bOX9e" id="6qR6GZqeRO_" role="TxmiU">
      <property role="2RkwnN" value="currency" />
      <property role="TrG5h" value="currency" />
      <node concept="Xl_RD" id="6qR6GZqeROM" role="2CNmdP">
        <property role="Xl_RC" value="Currency" />
      </node>
      <node concept="17QB3L" id="6qR6GZqeRSe" role="2RkE6I" />
      <node concept="2RoN1w" id="6qR6GZqeROO" role="2RnVtd">
        <node concept="3wEZqW" id="6qR6GZqeROS" role="3wFrgM" />
        <node concept="3xqBd$" id="6qR6GZqeROT" role="3xrYvX">
          <node concept="3Tm1VV" id="6qR6GZqeROV" role="3xqFEP" />
        </node>
      </node>
      <node concept="3Tm1VV" id="6qR6GZqeROW" role="1B3o_S" />
    </node>
    <node concept="1bOX9e" id="6qR6GZqeROX" role="TxmiU">
      <property role="2RkwnN" value="status" />
      <property role="TrG5h" value="status" />
      <node concept="Xl_RD" id="6qR6GZqeRPa" role="2CNmdP">
        <property role="Xl_RC" value="Invoice status" />
      </node>
      <node concept="2XvVpB" id="6qR6GZqeRPb" role="2RkE6I">
        <ref role="3$lB4D" node="6qR6GZqdTsJ" resolve="InvoiceStatus" />
      </node>
      <node concept="2RoN1w" id="6qR6GZqeRPc" role="2RnVtd">
        <node concept="3wEZqW" id="6qR6GZqeRPg" role="3wFrgM" />
        <node concept="3xqBd$" id="6qR6GZqeRPh" role="3xrYvX">
          <node concept="3Tm1VV" id="6qR6GZqeRPj" role="3xqFEP" />
        </node>
      </node>
      <node concept="3Tm1VV" id="6qR6GZqeRPk" role="1B3o_S" />
    </node>
  </node>
  <node concept="12nvSr" id="6qR6GZqeV4I">
    <property role="TrG5h" value="InvoicePersistence" />
    <property role="3GE5qa" value="persistence" />
    <node concept="12nEzA" id="6qR6GZqeV4O" role="12nEwW">
      <property role="TrG5h" value="InvoiceMapping" />
      <ref role="12nOxz" node="6qR6GZqdTq8" resolve="Invoice" />
      <node concept="Xl_RD" id="6qR6GZqeV4R" role="12gAQd">
        <property role="Xl_RC" value="T_INVOICE" />
      </node>
      <node concept="jyGaT" id="6qR6GZqeV4S" role="jyGaQ" />
      <node concept="12nEzJ" id="6qR6GZqeV4W" role="3caO6$">
        <ref role="12nL8z" node="6qR6GZqdTqf" resolve="id" />
        <node concept="Xl_RD" id="6qR6GZqeV4Y" role="12k7lF">
          <property role="Xl_RC" value="ID" />
        </node>
      </node>
      <node concept="12nEzJ" id="6qR6GZqeV51" role="3caO6$">
        <ref role="12nL8z" node="6qR6GZqeRL_" resolve="invoiceNumber" />
        <node concept="Xl_RD" id="6qR6GZqeV53" role="12k7lF">
          <property role="Xl_RC" value="INVOICE_NUMBER" />
        </node>
      </node>
      <node concept="12nEzJ" id="6qR6GZqeV56" role="3caO6$">
        <ref role="12nL8z" node="6qR6GZqeRLX" resolve="issueDate" />
        <node concept="Xl_RD" id="6qR6GZqeV58" role="12k7lF">
          <property role="Xl_RC" value="ISSUE_DATE" />
        </node>
      </node>
      <node concept="12nEzJ" id="6qR6GZqeV5b" role="3caO6$">
        <ref role="12nL8z" node="6qR6GZqeRMl" resolve="dueDate" />
        <node concept="Xl_RD" id="6qR6GZqeV5d" role="12k7lF">
          <property role="Xl_RC" value="DUE_DATE" />
        </node>
      </node>
      <node concept="12nEzJ" id="6qR6GZqeV5g" role="3caO6$">
        <ref role="12nL8z" node="6qR6GZqeRMH" resolve="customerName" />
        <node concept="Xl_RD" id="6qR6GZqeV5i" role="12k7lF">
          <property role="Xl_RC" value="CUSTOMER_NAME" />
        </node>
      </node>
      <node concept="12nEzJ" id="6qR6GZqeV5l" role="3caO6$">
        <ref role="12nL8z" node="6qR6GZqeRN5" resolve="billingAddress" />
        <node concept="Xl_RD" id="6qR6GZqeV5n" role="12k7lF">
          <property role="Xl_RC" value="BILLING_ADDRESS" />
        </node>
      </node>
      <node concept="12nEzJ" id="6qR6GZqeV5q" role="3caO6$">
        <ref role="12nL8z" node="6qR6GZqeRNt" resolve="netAmount" />
        <node concept="Xl_RD" id="6qR6GZqeV5s" role="12k7lF">
          <property role="Xl_RC" value="NET_AMOUNT" />
        </node>
      </node>
      <node concept="12nEzJ" id="6qR6GZqeV5v" role="3caO6$">
        <ref role="12nL8z" node="6qR6GZqeRNP" resolve="taxAmount" />
        <node concept="Xl_RD" id="6qR6GZqeV5x" role="12k7lF">
          <property role="Xl_RC" value="TAX_AMOUNT" />
        </node>
      </node>
      <node concept="12nEzJ" id="6qR6GZqeV5$" role="3caO6$">
        <ref role="12nL8z" node="6qR6GZqeROd" resolve="totalAmount" />
        <node concept="Xl_RD" id="6qR6GZqeV5A" role="12k7lF">
          <property role="Xl_RC" value="TOTAL_AMOUNT" />
        </node>
      </node>
      <node concept="12nEzJ" id="6qR6GZqeV5D" role="3caO6$">
        <ref role="12nL8z" node="6qR6GZqeRO_" resolve="currency" />
        <node concept="Xl_RD" id="6qR6GZqeV5F" role="12k7lF">
          <property role="Xl_RC" value="CURRENCY" />
        </node>
      </node>
      <node concept="12nEzJ" id="6qR6GZqeV5I" role="3caO6$">
        <ref role="12nL8z" node="6qR6GZqeROX" resolve="status" />
        <node concept="Xl_RD" id="6qR6GZqeV5K" role="12k7lF">
          <property role="Xl_RC" value="STATUS" />
        </node>
      </node>
    </node>
  </node>
  <node concept="DXQ2w" id="6qR6GZqeV8W">
    <property role="TrG5h" value="InvoiceRepository" />
    <property role="jj94n" value="InvoiceRepository" />
    <property role="2Lvdk3" value="InvoiceRepository" />
    <property role="3n5e7y" value="true" />
    <property role="3GE5qa" value="persistence" />
    <node concept="3Tm1VV" id="6qR6GZqeV8Y" role="1B3o_S" />
    <node concept="DXQ2B" id="6qR6GZqeVaI" role="jymVt">
      <property role="2a4t7v" value="3PtsrckEx4q/CHECKIN" />
      <property role="TrG5h" value="checkin" />
      <property role="2Lvdk3" value="checkin" />
      <node concept="3cqZAl" id="6qR6GZqeVaM" role="3clF45" />
      <node concept="37vLTG" id="6qR6GZqeVaN" role="3clF46">
        <property role="TrG5h" value="invoice" />
        <property role="2Lvdk3" value="invoice" />
        <node concept="3uibUv" id="6qR6GZqeVaP" role="1tU5fm">
          <ref role="3uigEE" node="6qR6GZqdTq8" resolve="Invoice" />
        </node>
      </node>
      <node concept="3clFbS" id="6qR6GZqeVaQ" role="3clF47">
        <node concept="P1rGi" id="6qR6GZqeVaR" role="3cqZAp">
          <ref role="P14SV" node="6qR6GZqeV4O" resolve="InvoiceMapping" />
          <node concept="37vLTw" id="6qR6GZqeVaT" role="P1rGp">
            <ref role="3cqZAo" node="6qR6GZqeVaN" resolve="invoice" />
          </node>
        </node>
      </node>
      <node concept="3Tm1VV" id="6qR6GZqeVaU" role="1B3o_S" />
    </node>
    <node concept="1o6$dd" id="XNEDnbIGIx" role="jymVt" />
    <node concept="DXQ2B" id="6qR6GZqeVaV" role="jymVt">
      <property role="2a4t7v" value="3PtsrckEx4n/CHECKOUT" />
      <property role="TrG5h" value="checkout" />
      <property role="2Lvdk3" value="checkout" />
      <node concept="3uibUv" id="6qR6GZqeVaZ" role="3clF45">
        <ref role="3uigEE" node="6qR6GZqdTq8" resolve="Invoice" />
      </node>
      <node concept="37vLTG" id="6qR6GZqeVb0" role="3clF46">
        <property role="TrG5h" value="id" />
        <property role="2Lvdk3" value="id" />
        <node concept="10Oyi0" id="6qR6GZqeVb2" role="1tU5fm" />
      </node>
      <node concept="3clFbS" id="6qR6GZqeVb3" role="3clF47">
        <node concept="3clFbF" id="6qR6GZqeVb4" role="3cqZAp">
          <node concept="jybIQ" id="6qR6GZqeVb6" role="3clFbG">
            <property role="HScZ5" value="false" />
            <ref role="P14SV" node="6qR6GZqeV4O" resolve="InvoiceMapping" />
            <node concept="TUlRj" id="6qR6GZqeVb8" role="jxX7b">
              <node concept="37vLTw" id="6qR6GZqeVba" role="TUlRy">
                <ref role="3cqZAo" node="6qR6GZqeVb0" resolve="id" />
              </node>
            </node>
          </node>
        </node>
      </node>
      <node concept="3Tm1VV" id="6qR6GZqeVbb" role="1B3o_S" />
    </node>
    <node concept="DXQ2B" id="6qR6GZqeVbc" role="jymVt">
      <property role="TrG5h" value="findAll" />
      <property role="2Lvdk3" value="findAll" />
      <node concept="_YKpA" id="6qR6GZqeVbg" role="3clF45">
        <node concept="3uibUv" id="6qR6GZqeVbi" role="_ZDj9">
          <ref role="3uigEE" node="6qR6GZqdTq8" resolve="Invoice" />
        </node>
      </node>
      <node concept="3clFbS" id="6qR6GZqeVbj" role="3clF47">
        <node concept="3clFbF" id="6qR6GZqeVbk" role="3cqZAp">
          <node concept="jybIQ" id="6qR6GZqeVbm" role="3clFbG">
            <property role="HScZ5" value="true" />
            <ref role="P14SV" node="6qR6GZqeV4O" resolve="InvoiceMapping" />
          </node>
        </node>
      </node>
      <node concept="3Tm1VV" id="6qR6GZqeVbo" role="1B3o_S" />
    </node>
  </node>
  <node concept="3ugp7m" id="XNEDnbIGQQ">
    <property role="1ptSWV" value="R_Y55k$Btz/OVERWRITE_FORCED" />
    <node concept="3ugp7q" id="XNEDnbIGQZ" role="3ug97V">
      <property role="TrG5h" value="Page_0" />
      <node concept="20qEzJ" id="XNEDnbIGR0" role="10qiF$">
        <node concept="3clFbS" id="XNEDnbIGR1" role="2VODD2" />
      </node>
      <node concept="3063JU" id="XNEDnbIGR2" role="3063Jp" />
    </node>
  </node>
</model>

