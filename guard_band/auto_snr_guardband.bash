GNURADIO_FOLDER="../../fg-stuff";
AMPLITUDES=(0.1 0.5 1.0)
AMPLITUDES=(0.0 )

for amplitude in  ${AMPLITUDES[@]}; do
    #change amplitude in configuration fil
    sed -i "s/amplitude2.*$/amplitude2 =${amplitude}/g" ${GNURADIO_FOLDER}/default

    bash ${GNURADIO_FOLDER}/cp_to_containers.sh

    for it in `seq 0 2`; do
        python do_usrp_tests_2pcs.py "_${amplitude/./}_${it}"
    done

    fol="${amplitude/./_}"
    mkdir ./$fol
    scp connect@192.168.10.30:~/fg-stuff/rx_9*_${amplitude/./}_${it} $fol

    python ../parse_bins.py --batch --src-folder $fol --dst-folder $fol --csv-file $fol/csv.csv --gen-img --gen-csv

    awk '{
      snr[$1] += $4;
      snrq[$1] += $4 ^ 2;
      count[$1] += 1;
    }
    END{
      for (a in snr) {
          print a " " snr[a]/count[a] " " sqrt((snrq[a]-snr[a]^2/count[a])/count[a]);
      }
    }' $fol/csv.csv | sort > $fol/plottable.csv
done
