* def path = 'classpath:data/xml/DVS/retrieveMtnDetails.xml'
* def FileUtils = Java.type('org.apache.commons.io.FileUtils')
* def File = Java.type('java.io.File')
* def xmlString = FileUtils.readFileToString(new File(karate.toAbsolutePath(path)), 'UTF-8')
* def encoded = karate.urlEncode(xmlString)

* header Content-Type = 'application/x-www-form-urlencoded'
* request 'xml=' + encoded
* method post
* status 200
* print response