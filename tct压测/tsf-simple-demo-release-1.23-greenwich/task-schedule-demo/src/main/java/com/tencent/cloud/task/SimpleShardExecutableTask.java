package com.tencent.cloud.task;

import com.tencent.cloud.task.sdk.client.model.ExecutableTaskData;
import com.tencent.cloud.task.sdk.client.model.ProcessResult;
import com.tencent.cloud.task.sdk.client.spi.ExecutableTask;
import com.tencent.cloud.task.sdk.common.protocol.message.ShardingArgs;
import com.tencent.cloud.task.sdk.common.protocol.message.TaskExecuteMeta;
import com.tencent.cloud.task.sdk.core.utils.ThreadUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.lang.invoke.MethodHandles;

public class SimpleShardExecutableTask implements ExecutableTask {

    private final static Logger LOG = LoggerFactory.getLogger(MethodHandles.lookup().lookupClass());

    @Override
    public ProcessResult execute(ExecutableTaskData executableTaskData) {
        ShardingArgs shardingArgs = executableTaskData.getShardingArgs();
        TaskExecuteMeta executeMeta = executableTaskData.getTaskMeta();
        LOG.info("executeMetaJson:{}",executeMeta.toString());
        Integer shardingKey = shardingArgs.getShardKey();
        String shardingValue = shardingArgs.getShardValue();
        LOG.info("shardingKey: {},shardingValue: {}", shardingKey,shardingValue);
        // 执行3秒
        ThreadUtils.waitMs(3000L);

        return ProcessResult.newSuccessResult();
    }
}
