import gzip
import os
import argparse

def findProxy(in_gwas, out_gwas):
	gwas_id = set()
	with open(in_gwas) as gwas_file:
    		for line in gwas_file:
			if line.split("\t")[2] not in ["snp","SNP"]:
        			gwas_id.add(line.split("\t")[2])

	ref_id = set()
	with gzip.open('/udd/remhc/bin/snpsea/TGP2011.bed.gz', 'rb') as ref_file:
    		for line in ref_file:
        		ref_id.add(line.rstrip('\n').split("\t")[3])
#	print gwas_id
#	print ref_id

#	gwas_index_id = [item for item in gwas_id if item not in ref_id]

	gwas_index_id = gwas_id - ref_id

#	print gwas_index_id
#	print len(gwas_index_id)

	changed_id = []
	proxy_id = []
	proxy_chr = []
	proxy_pos = []
	proxy_rsqr = []
	for index_id in gwas_index_id:
		temp_LDproxy = index_id + "_temp_LDproxy"
		cmd_LDproxy = "curl -s -k -X GET 'https://analysistools.nci.nih.gov/LDlink/LDlinkRest/ldproxy?var={0}&pop=CEU&r2_d=r2'".format(index_id)+ ">" +  temp_LDproxy
		os.system(cmd_LDproxy)
		with open(temp_LDproxy, 'r') as LDproxy_file:
				for line in LDproxy_file:
					if "{" in line:
                        			print index_id, "is not in 1000G reference panel"
						break	
					elif 'RS_Number' not in line:
						temp_id = line.split("\t")[0]
						r_sqr = line.split("\t")[6]
						if temp_id !=index_id:
							if temp_id in ref_id:			
								proxy_id.append(temp_id)
								proxy_chr.append((line.split("\t")[1]).split(":")[0])
								proxy_pos.append((line.split("\t")[1]).split(":")[1])
								proxy_rsqr.append((line.split("\t")[6]))
								changed_id.append(index_id)
#									print index_id, " proxy_id: ", proxy_id, " proxy_chr: ", proxy_chr, " proxy_pos: ", proxy_pos
								
								break
#							else:
#									print index_id, " has no proxy with R^2 > 0.8"
#								break
	
						elif temp_id not in ref_id:
							if float(r_sqr) < 0.8:
#								print index_id, " has no proxy with R^2 > 0.8"
								break
#				elif temp_id not in ref_id:
#					print index_id, " has no proxy in reference"	
#		print "index_id: ", index_id, " proxy_id: ", proxy_id, " proxy_chr: ", proxy_chr, " proxy_pos: ", proxy_pos
		os.remove(temp_LDproxy)
#	print "changed id: ", changed_id, "proxy_id: ", proxy_id	

	keep_p = []

	for item in changed_id:
		with open(in_gwas, 'r') as gwas_file:
			for line in gwas_file:
        			if line.split("\t")[2]==item: 
					keep_p.append(line.rstrip('\n').split("\t")[3])


#	print keep_p

	headers = ['chr', 'pos', 'snp', 'P', 'R2']
	outFile = open(out_gwas, 'wb')
	outFile.write('\t'.join(headers) + '\n')
	for i in range(len(proxy_id)):
    		outFile.write("%s\t%s\t%s\t%s\t%s\n" % (proxy_chr[i], proxy_pos[i], proxy_id[i], keep_p[i], proxy_rsqr[i]))

	with open(in_gwas, 'r') as gwas_file:
		for line in gwas_file:
			if line.split("\t")[2] not in ['snp', 'SNP'] and line.split("\t")[2] not in changed_id:
				outFile.write(line.rstrip('\n')+"\tNA\n")

	outFile.close()

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description = "Find and replace with proxy SNPs")
	parser.add_argument("--input", required = True, help = "Original SNPsea gwas file")
	parser.add_argument("--output", required = True, help = "Output SNPsea gwas file")
	args = vars(parser.parse_args())
	inFile = args["input"]
	outFile = args["output"]

	findProxy(inFile, outFile)

